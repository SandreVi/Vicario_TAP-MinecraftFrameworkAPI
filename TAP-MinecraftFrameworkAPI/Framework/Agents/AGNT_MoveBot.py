from Framework.Utils.agent import Agent

DEFAULT_WALK = 1
DEFAULT_JUMP = 1
class MoveBot(Agent):

    def cmd_walk(self, *args):
        help_message = [
            "-> ЛЕЛАР {nSteps}: Бот ловзархо 'nSteps' хьалха дӀахьур ву.",
            "Example: ЛЕЛАР 5"
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
        # args[0] дерриге терахье дерзо хьажа
        if args:
            steps = self.convert_to_int(args[0])
            if steps is None:
                self.mc.postToChat(f"ГӀалаташ: '{args[0]}' нийса терахь дац гӀулчашна.")
                return
        else:
            steps = DEFAULT_WALK

        direction = self.get_player_orientation()
        x, y, z = self.where()
        x, z, y, _, _ = self.calculate_position(x, z, y, direction, False, steps)
        self.move(x, y, z)

    def jump_height(self, *args):
        # args[0] дерриге терахье дерзо хьажа
        if args:
            height = self.convert_to_int(args[0])
            if height is None:
                self.mc.postToChat(f"ГӀалаташ: '{args[0]}' локхаллин нийса терахь дац.")
                return
        else:
            height = DEFAULT_WALK

        if height is None:
            self.mc.postToChat(f"ГӀалаташ: '{args[0]}' нийса терахь дац кхиссаваларан локхаллина.")
            return

        x, y, z = self.where()
        y += height
        self.move(x, y, z)

    # Функци мах дерриге терахье дерзоран .
    def convert_to_int(self, value):
        """
        Converts a value to an integer if possible.
        If it cannot be converted, returns None.
        """
        try:
            return int(value)
        except ValueError:
            return None
