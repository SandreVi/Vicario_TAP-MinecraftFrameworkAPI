import time
import importlib
import os
import inspect
from Framework.Utils.chat_listener import ChatListener

class AgentManager(ChatListener):
    def __init__(self, mc):
        """
        Initializes the AgentManager, which manages the agents and listens for chat commands.
        :param mc: Minecraft connection instance.
        """
        super().__init__(mc)
        self.agents = {}  # Dictionary to hold agent names and their corresponding instances
        self.commands = {}  # Dictionary to hold commands and their corresponding agent methods

    def import_agents(self):
        """
        Dynamically imports agents from the 'Agents' folder and registers their commands.
        """
        # Path where the agent files are located
        agents_path = os.path.join(os.path.dirname(__file__), 'Agents')
        
        # List all the agent files in the folder and filter the ones that start with "AGNT_" and end with ".py"
        agent_files = filter(lambda filename: filename.startswith("AGNT_") and filename.endswith(".py"), os.listdir(agents_path))

        # Process each valid agent file
        for filename in agent_files:
            agent_name = filename[:-3]  # We remove the '.py' extension to get the class name
            agent_module = importlib.import_module(f"Framework.Agents.{agent_name}")
            
            # Try to dynamically get the class from the module (CLASS NAME MUST MATCH THE FILE SUFFIX)
            class_name = agent_name.split("_")[1]  # Take the class name after "AGNT_"
            try:
                agent_class = getattr(agent_module, class_name)  # Get the class from the module
            except AttributeError:
                print(f"Error: Module {agent_name} does not have a class named {class_name}.")
                continue
            
            # Create an instance of the agent class
            agent_instance = agent_class(self.mc)  # Instantiate the agent
            
            # Call the agent's import method to register its commands
            agent_commands = agent_instance.import_()
            
            # Register the commands and methods
            for command, method in agent_commands:
                self.commands[command] = method  # Map command to the corresponding method
            
            # Store the agent instance
            self.agents[agent_name] = agent_instance

    def process_message(self, command):
        """
        Processes the received chat message and executes the corresponding method if it's valid.
        """
        if command is None:
            self.mc.postToChat("Too much idle time... Framework shutting down!")
            return

        # Split the message into all individual parts (words) and remove leading/trailing spaces
        parts = command.split()  # This will split the command and parameters correctly
        command = parts[0].upper()  # Convert the command to uppercase for consistency
        params = parts[1:]  # Get all parameters except the command

        # Dictionary-based "switch" for command handling
        command_actions = {
            "CMDLIST": lambda: self.mc.postToChat("Available commands: " + ", ".join(self.commands.keys())),
            "COMMANDLIST": lambda: self.mc.postToChat("Available commands: " + ", ".join(self.commands.keys())),
            "HELP": lambda: [
                self.mc.postToChat("->CMDLIST/COMMANDLIST: Show available commands for agents"),
                self.mc.postToChat("->RELOAD: Refresh loaded agents from Agents folder"),
                self.mc.postToChat("->END/STOP: Close framework"),
                self.mc.postToChat("->HELP: This command! (pretty self-explanatory)")
            ],
            "RELOAD": lambda: [
                self.agents.clear(),
                self.commands.clear(),
                self.import_agents(),
                self.mc.postToChat("Agents reloaded!")
            ],
            "END": lambda: self.mc.postToChat("To properly abort, JUST type \"END\" or \"STOP\" with no extra parameters"),
            "STOP": lambda: self.mc.postToChat("To properly abort, JUST type \"END\" or \"STOP\" with no extra parameters")
        }

        # Default case for agent-based commands
        if command in command_actions:
            command_actions[command]()  # Execute the corresponding action
        elif command in self.commands:
            method = self.commands[command]
            method(*params)
        else:
            self.mc.postToChat(f"Command '{command}' not recognized.")

    def start(self, timeout_enabled=True, timeout=10):
        """
        Initializes the agent manager, imports the agents, and starts listening for chat commands.
        """
        # Import agents and their commands
        self.import_agents()

        self.mc.postToChat("Agents imported! Listening...")
        self.mc.postToChat("Type \"HELP\" if needed!")

        # Start listening for chat commands
        self.listen_for_chat_commands(self, timeout_enabled, timeout)  # Call the listen_for_chat_commands method of ChatListener

        # Goodbye message
        self.mc.postToChat("Framework closed!")
