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
        API-наш мотт охьал дӀарг дийца Minecraft-га.
        """
        self.mc = mc

    def talk(self, message):
        """
        Оьрхан чунчо куьна Майнкрафт чат.
        
        :param message: Чуьна Майнкрафт чат-га оьрхан чунчо.
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
        Цхьам аьржа хечу, юхаларгий оркхой аук.
        """
        # Игрок къаттнаш (0° - 360°)
        player_rotation = self.mc.player.getRotation()

        # Ротациийн адо 0-дан 360-га хьо хи кхеташ
        rotation = player_rotation % 360
        
        # Дехар ротацииг каарш, оркхой хорщин
        # Ротациийн маьршу -> [0, 360]
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
        Позиций генерациа я шекъяр, хила хьалалха 3 позиция.
        Дахареш чучарха [(x1, z1, y1), (x2, z2, y2), (x3, z3, y3)]
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
        Оьрхан хила позиция, мотт ахала Анторшка изи позиция.
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
        Блок хила позиция, шекъярш редстоуну хи ахала.
        """
        # Дехар блок поддержки хила
        if support_block_id:
            self.mc.setBlock(x, y - 1, z, support_block_id)

        # Основной блок хила
        self.mc.setBlock(x, y, z, block_id, 1 if activate_on_place else 0)

        # Анторшка изи редстоун, блок хила
        if add_redstone and xTorch is not None and zTorch is not None:
            if support_block_id:
                self.mc.setBlock(xTorch, y - 1, zTorch, support_block_id)
            self.mc.setBlock(xTorch, y, zTorch, REDSTONE_TORCH_ID)
