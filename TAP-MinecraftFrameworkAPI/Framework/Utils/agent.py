from Framework.API.mcBotAPI import mcBotAPI

class Agent(mcBotAPI):

    def __init__(self, mc):
        """
        Initializes the agent and stores the mc (Minecraft connection).
        :param mc: The Minecraft connection instance.
        """
        mcBotAPI.__init__(self, mc)

    def import_(self):
        """
        Returns the commands this agent handles, along with the corresponding methods.
        Only methods prefixed with 'cmd_' are considered valid commands.
        """
        prefix = "cmd_"  # Define the prefix that commands will start with

        # Create a list of tuples where:
        # - The first element is the command name in uppercase, without the "cmd_" prefix
        # - The second element is the reference to the method that handles that command
        return [
            # Iterate over all attributes and methods of the current object (self)
            (cmd[len(prefix):].upper(), getattr(self, cmd))  # This line creates a tuple with the command name (without "cmd_" and in uppercae) and its associated method
            for cmd in dir(self)  # Iterate over all attributes and methods of the object
            if callable(getattr(self, cmd, None))  # Check if the attribute is callable -> it's a method
            and cmd.startswith(prefix)  # Check if the attribute name starts with the "cmd_" prefix
        ] 

    def execute_cmd(self, help_message, actions, *args):
        """
        Handles command execution by checking for 'HELP' and executing the correct action.
        
        :param help_message: The help text to display if 'HELP' is requested
        :param actions: Dictionary mapping commands to functions
        :param args: Command arguments (tuple)
        """
        # Check if args is not empty and if the first argument is "HELP"
        if args and isinstance(args[0], str) and args[0].upper() == "HELP" and len(args) == 1:
            self._show_help(help_message)
            return

        # Execute the action
        self._execute_action(actions, *args)  # Pass *args to _execute_action

    def _show_help(self, help_message):
        """
        Displays the help message in the chat.
        """
        for line in help_message:
            self.talk(line)

    def _execute_action(self, actions, *args):
        """
        Executes the action corresponding to the command argument.
        """
        if args:  # Check if args is not empty
            # Get the first argument in uppercase (corresponds to the command)
            command = args[0].upper()

            # Look for the corresponding action
            action = actions.get(command)

            if action:
                # Execute the action with the remaining arguments
                action(*args[1:])
            else:
                # If the action doesn't exist, check for a default action
                if not self._check_default(actions, *args):
                    self.talk(f"Invalid parameter: {args[0]}. Use command + HELP for available options.")  # Changed to self.talk
        else:  # If args is empty
            # If args[0] doesn't exist, check if there's a default action
            if not self._check_default(actions, *args):
                self.talk("This command expects parameters! Use command + HELP for available options.")  # Changed to self.talk

    def _check_default(self, actions, *args):
        """
        Checks if there is a default action in the actions dictionary and executes it.
        Returns True if the default action was executed, False otherwise.
        """
        default_action = actions.get("DEFAULT")
        if default_action:
            default_action(*args)  # Execute the default action, passing the arguments
            return True  # Indicate that the default action was executed
        return False  # Indicate that no default action was found
