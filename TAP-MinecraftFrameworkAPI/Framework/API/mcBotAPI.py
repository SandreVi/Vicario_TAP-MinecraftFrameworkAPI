import random
from MyAdventures.mcpi.minecraft import Minecraft
from MyAdventures.mcpi import block
from MyAdventures.mcpi.vec3 import Vec3

REDSTONE_TORCH_ID = 76
MIN_RANDOM = 1
MAX_RANDOM = 3

class mcBotAPI:
    
    def __init__(self, mc):
        """
        Inicializa la API con la conexión a Minecraft.
        """
        self.mc = mc

    def talk(self, message):
        """
        Sends a message to the Minecraft chat.
        
        :param message: The message to be sent to the Minecraft chat.
        """
        self.mc.postToChat(message)

    def move(self, x, y, z):
        position = Vec3(x, y, z)
        self.mc.player.setTilePos(position)

    def where(self):
        player_pos = self.mc.player.getTilePos()
        return player_pos.x, player_pos.y, player_pos.z
        
    def get_player_orientation(self):
        """
        Returns the direction the player is facing in English (NORTH, WEST, SOUTH, EAST).
        """
        # Get the player's rotation (0° - 360°)
        player_rotation = self.mc.player.getRotation()

        # Normalize the rotation to be in the range of 0 to 360
        rotation = player_rotation % 360
        
        # Determine the player's facing direction based on the rotation
        # rotation values -> [0, 360]
        if rotation >= 315 or rotation < 45:
            return "SOUTH"
        elif 45 <= rotation < 135:
            return "WEST"
        elif 135 <= rotation < 225:
            return "NORTH"
        else: # elif 225 <= rotation < 315:
            return "EAST"

    def arrange_positions(self):
        """
        Generates three positions (base + dos random near the player).
        Retunrs a list with coordinates [(x1, z1, y1), (x2, z2, y2), (x3, z3, y3)]
        """
        x, y, z = self.where()

        positions = [
            (x, z),
            (x + random.choice([MIN_RANDOM, MAX_RANDOM]), z + random.choice([MIN_RANDOM, MAX_RANDOM])),
            (x + random.choice([MIN_RANDOM, MAX_RANDOM]), z + random.choice([MIN_RANDOM, MAX_RANDOM]))
        ]

        return [(x, z, y) for x, z in positions]

    def calculate_position(self, x, z, y, rotation, add_redstone, block_distance=5):
        """
        Calculates the final position of the block and the redstone torch based on the orientation.
        """
        if rotation == "EAST":
            x += block_distance
            xTorch, zTorch = (x + 1, z) if add_redstone else (None, None)
        elif rotation == "WEST":
            x -= block_distance
            xTorch, zTorch = (x - 1, z) if add_redstone else (None, None)
        elif rotation == "NORTH":
            z -= block_distance
            xTorch, zTorch = (x, z - 1) if add_redstone else (None, None)
        elif rotation == "SOUTH":
            z += block_distance
            xTorch, zTorch = (x, z + 1) if add_redstone else (None, None)
        else:
            xTorch, zTorch = None, None

        return x, z, y, xTorch, zTorch

    def place_block(self, x, z, y, xTorch, zTorch, block_id, add_redstone, support_block_id=None, activate_on_place=False):
        """
        Coloca un bloque en una posición dada, con opción de soporte y redstone.
        """
        # Colocar bloque de soporte si es necesario
        if support_block_id:
            self.mc.setBlock(x, y - 1, z, support_block_id)

        # Colocar el bloque principal
        self.mc.setBlock(x, y, z, block_id, 1 if activate_on_place else 0)

        # Si se requiere redstone, colocamos la antorcha con su soporte
        if add_redstone and xTorch is not None and zTorch is not None:
            if support_block_id:
                self.mc.setBlock(xTorch, y - 1, zTorch, support_block_id)
            self.mc.setBlock(xTorch, y, zTorch, REDSTONE_TORCH_ID)
