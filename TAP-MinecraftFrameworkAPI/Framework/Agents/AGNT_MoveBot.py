from Framework.Utils.agent import Agent

DEFAULT_WALK = 1
DEFAULT_JUMP = 1
class MoveBot(Agent):

    def cmd_walk(self, *args):
        help_message = [
            "-> WALK {nSteps}: The bot will move the player 'nSteps' forward.",
            "Example: WALK 5"
        ]

        actions = {
            "DEFAULT": self.walk_steps
        }

        self.execute_cmd(help_message, actions, *args)

    def cmd_jump(self, *args):
        help_message = [
            "-> JUMP {height}: The bot will make the player jump 'height' blocks.",
            "Example: JUMP 5"
        ]

        actions = {
            "DEFAULT": self.jump_height
        }

        self.execute_cmd(help_message, actions, *args)  

    def walk_steps(self, *args):
        # Try to convert args[0] to an integer
        if args:
            steps = self.convert_to_int(args[0])
            if steps is None:
                self.mc.postToChat(f"Error: '{args[0]}' is not a valid number for steps.")
                return
        else:
            steps = DEFAULT_WALK

        direction = self.get_player_orientation()
        x, y, z = self.where()
        x, z, y, _, _ = self.calculate_position(x, z, y, direction, False, steps)
        self.move(x, y, z)

    def jump_height(self, *args):
        # Try to convert args[0] to an integer
        if args:
            height = self.convert_to_int(args[0])
            if height is None:
                self.mc.postToChat(f"Error: '{args[0]}' is not a valid number for height.")
                return
        else:
            height = DEFAULT_WALK

        if height is None:
            self.mc.postToChat(f"Error: '{args[0]}' is not a valid number for jump height.")
            return

        x, y, z = self.where()
        y += height
        self.move(x, y, z)

    # Function to convert a value to an integer
    def convert_to_int(self, value):
        """
        Converts a value to an integer if possible.
        If it cannot be converted, returns None.
        """
        try:
            return int(value)
        except ValueError:
            return None
