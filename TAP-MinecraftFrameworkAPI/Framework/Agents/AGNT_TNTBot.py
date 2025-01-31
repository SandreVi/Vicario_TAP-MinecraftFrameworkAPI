import random
from MyAdventures.mcpi.block import TNT, GLASS
from Framework.Utils.agent import Agent

REDSTONE_TORCH_ID = 76  # block_id цӀен тӀулган лампа
MIN_RANDOM = 1
MAX_RANDOM = 3
BLOCK_DISTANCE = 5

class TNTBot(Agent):

    def cmd_deploy(self, *args):
        """
        Тротил автоматически я ручной режимехь дӀахӀоттае, еллачу параметрашна тӀе а тевжаш.
        """
        help_message = [
            "-> DEPLOY {АВТО/РУЧНОСТЬ} Тротил блок 5 блок генахь а, кхин а 2 ларамаза меттигашкахь дӀахӀоттадо.",
            "* АВТО: Блокаш дӀахӀиттийначул тӀаьхьа сихха цӀе латтор ю.",
            "* РУЧНОСТЬ: Блокаш ловзархочо юкъаметтиг лелийча цӀе латтор ю."
        ]
            
        actions = {
            "АВТО": self.auto_mode,
            "РУЧНОСТЬ": self.manual_mode
        }
        
        self.execute_cmd(help_message, actions, *args)

    def auto_mode(self, *args):
        """
        Тротил автоматически дӀанисъе цӀен тӀулган лампаца.
        """
        self.deploy_tnts(add_redstone=True)

    def manual_mode(self, *args):
        """
        ДӀанисде ТНТ ручной плеер хьажа.
        """
        self.deploy_tnts(add_redstone=False)

    def deploy_tnts(self, add_redstone):
        """
        Генераци йо позицешца а, дӀахӀиттадо ТНТ блокаш `mcAPI` йолуш, я АВТО я РУЧНИ режимехь.
        """
        # Ловзархочун ориентаци схьаэца (уьш дуьхьал болчу агӀор)
        direction = self.get_player_orientation()

        # Тротил дӀахӀоттор йолчу базан позицеш генерировать е .
        positions = self.arrange_positions()

        calculated_positions = [
            self.calculate_position(x, z, y, direction, add_redstone) for x, z, y in positions
        ]

        for pos in calculated_positions:
            self.place_block(*pos, block_id=TNT.id, add_redstone=add_redstone, support_block_id=GLASS.id, activate_on_place=not add_redstone)



