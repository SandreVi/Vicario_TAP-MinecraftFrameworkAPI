# AGNT_TNTBot.py
import random
from MyAdventures.mcpi.block import TNT, GLASS
from Framework.Utils.agent import Agent

REDSTONE_TORCH_ID = 76  # block_id for redstone torch
MIN_RANDOM = 1
MAX_RANDOM = 3
BLOCK_DISTANCE = 5

class TNTBot(Agent):

    def cmd_deploy(self, *args):
        """
        Deploy TNT in auto or manual mode based on the provided parameters.
        """
        help_message = [
            "-> DEPLOY {AUTO/MANUAL} Places a TNT block 5 blocks away and 2 additional in random positions.",
            "* AUTO: Blocks will ignite immediately after placement.",
            "* MANUAL: Blocks will ignite when interacted with by the player."
        ]
            
        actions = {
            "AUTO": self.auto_mode,
            "MANUAL": self.manual_mode
        }
        
        self.execute_cmd(help_message, actions, *args)

    def auto_mode(self, *args):
        """
        Arrange TNT automatically with redstone torch.
        """
        self.deploy_tnts(add_redstone=True)

    def manual_mode(self, *args):
        """
        Arrange TNT manually for player to click.
        """
        self.deploy_tnts(add_redstone=False)

    def deploy_tnts(self, add_redstone):
        """
        Generates positions and places TNT blocks with `mcAPI`, in either AUTO or MANUAL mode.
        """
        # Get the player's orientation (direction they are facing)
        direction = self.get_player_orientation()

        # Generate the base positions where TNT will be placed
        positions = self.arrange_positions()

        calculated_positions = [
            self.calculate_position(x, z, y, direction, add_redstone) for x, z, y in positions
        ]

        for pos in calculated_positions:
            self.place_block(*pos, block_id=TNT.id, add_redstone=add_redstone, support_block_id=GLASS.id, activate_on_place=not add_redstone)



