import unittest
from unittest.mock import MagicMock
from Framework.API.mcBotAPI import mcBotAPI
from MyAdventures.mcpi.vec3 import Vec3

class TestMcBotAPI(unittest.TestCase):

    # Это тесты для API, чтобы убедиться, что оно работает правильно.

    def setUp(self):
        self.mc_mock = MagicMock()

        self.bot_api = mcBotAPI(self.mc_mock)

    def test_talk(self):
        # Проверяем, что сообщение правильно отправляется в чат Minecraft.
        message = "Салам маршал ду шуьга, Майнкрафт!"
        self.bot_api.talk(message)
        self.mc_mock.postToChat.assert_called_with(message)

    def test_move(self):
        # Проверяем, что бот перемещается в указанную позицию.
        x, y, z = 10, 20, 30
        self.bot_api.move(x, y, z)
        self.mc_mock.player.setTilePos.assert_called_with(Vec3(x, y, z))

    def test_where(self):
        # Проверяем, что метод where возвращает правильные координаты игрока.
        self.mc_mock.player.getTilePos.return_value = Vec3(10, 20, 30)
        x, y, z = self.bot_api.where()
        self.assertEqual((x, y, z), (10, 20, 30))

    def test_get_player_orientation(self):
        # Проверяем, что метод get_player_orientation возвращает правильное направление.
        self.mc_mock.player.getRotation.return_value = 45
        orientation = self.bot_api.get_player_orientation()
        self.assertEqual(orientation, "WEST")

        self.mc_mock.player.getRotation.return_value = 135
        orientation = self.bot_api.get_player_orientation()
        self.assertEqual(orientation, "NORTH")

        self.mc_mock.player.getRotation.return_value = 225
        orientation = self.bot_api.get_player_orientation()
        self.assertEqual(orientation, "EAST")

        self.mc_mock.player.getRotation.return_value = 315
        orientation = self.bot_api.get_player_orientation()
        self.assertEqual(orientation, "SOUTH")

    def test_arrange_positions(self):
        # Проверяем метод arrange_positions, чтобы убедиться, что он генерирует позиции вокруг игрока.
        self.mc_mock.player.getTilePos.return_value = Vec3(10, 20, 30)
        self.bot_api.where = MagicMock(return_value=(10, 20, 30))

        positions = self.bot_api.arrange_positions()
        
        # Проверяем, что метод arrange_positions возвращает правильное количество позиций.
        self.assertEqual(len(positions), 3)
        self.assertTrue(all(isinstance(pos, tuple) and len(pos) == 3 for pos in positions))

    def test_calculate_position_north(self):
        # Проверяем метод calculate_position для направления NORTH.
        x, z, y = 10, 20, 30
        rotation = "NORTH"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        self.assertEqual(x, 10)  # x остаётся неизменным для направления NORTH
        self.assertEqual(z, 15)  # z уменьшается на block_distance (5) для NORTH
        self.assertEqual(y, 30)  # y остаётся неизменным
        self.assertEqual(xTorch, 10)  # x позиции для факела из красного камня
        self.assertEqual(zTorch, 14)  # z позиции факела из красного камня = z - 1

    def test_calculate_position_east(self):
        # Проверяем метод calculate_position для направления EAST.
        x, z, y = 10, 20, 30
        rotation = "EAST"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        # Проверяем, что метод учитывает изменение позиций при направлении EAST.
        self.assertEqual(x, 15)  # x увеличивается на block_distance (5) для EAST
        self.assertEqual(z, 20)  # z остаётся неизменным
        self.assertEqual(y, 30)  # y остаётся неизменным
        self.assertEqual(xTorch, 16)  # x позиции для факела из красного камня = x + 1
        self.assertEqual(zTorch, 20)  # z позиции факела из красного камня

    def test_calculate_position_south(self):
        # Проверяем метод calculate_position для направления SOUTH.
        x, z, y = 10, 20, 30
        rotation = "SOUTH"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        # Проверяем корректность финальной позиции в зависимости от направления и добавления факела из красного камня.
        self.assertEqual(x, 10)  # x остаётся неизменным
        self.assertEqual(z, 25)  # z увеличивается на block_distance (5) для SOUTH
        self.assertEqual(y, 30)  # y остаётся неизменным
        self.assertEqual(xTorch, 10)  # x позиции для факела из красного камня
        self.assertEqual(zTorch, 26)  # z позиции факела из красного камня = z + 1

    def test_calculate_position_west(self):
        # Проверяем метод calculate_position для направления WEST.
        x, z, y = 10, 20, 30
        rotation = "WEST"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        # Проверяем корректность финальной позиции в зависимости от направления и добавления факела из красного камня.
        self.assertEqual(x, 5)  # x уменьшается на block_distance (5) для WEST
        self.assertEqual(z, 20)  # z остаётся неизменным
        self.assertEqual(y, 30)  # y остаётся неизменным
        self.assertEqual(xTorch, 4)  # x позиции для факела из красного камня = x - 1
        self.assertEqual(zTorch, 20)  # z позиции факела из красного камня

    def test_place_block(self):
        # Проверяем метод place_block, чтобы убедиться, что блоки ставятся корректно.
        x, z, y = 10, 20, 30
        xTorch, zTorch = 11, 20
        block_id = 1
        support_block_id = 4
        add_redstone = True
        activate_on_place = False

        # Вызываем метод place_block
        self.bot_api.place_block(x, z, y, xTorch, zTorch, block_id, add_redstone, support_block_id, activate_on_place)

        # Проверяем, что методы API Minecraft были вызваны для установки блоков.
        self.mc_mock.setBlock.assert_any_call(x, y - 1, z, support_block_id)  # Блок поддержки на (x, y-1, z)
        self.mc_mock.setBlock.assert_any_call(x, y, z, block_id, 0)  # Основной блок на (x, y, z) без активации
        self.mc_mock.setBlock.assert_any_call(xTorch, y - 1, zTorch, support_block_id)  # Блок поддержки для факела из красного камня
        self.mc_mock.setBlock.assert_any_call(xTorch, y, zTorch, 76)  # Факел из красного камня на (xTorch, y, zTorch)
        
    def test_place_block_with_activation(self):
        # Проверяем метод place_block с активацией (activate_on_place=True).
        x, z, y = 10, 20, 30
        xTorch, zTorch = 11, 20
        block_id = 1
        support_block_id = 4
        add_redstone = True
        activate_on_place = True  # Включаем активацию вручную

        # Вызываем метод place_block
        self.bot_api.place_block(x, z, y, xTorch, zTorch, block_id, add_redstone, support_block_id, activate_on_place)

        # Проверяем, что методы API Minecraft были вызваны для установки блоков с активацией.
        self.mc_mock.setBlock.assert_any_call(x, y - 1, z, support_block_id)  # Блок поддержки на (x, y-1, z)
        self.mc_mock.setBlock.assert_any_call(x, y, z, block_id, 1)  # Основной блок на (x, y, z) с активацией (1)
        self.mc_mock.setBlock.assert_any_call(xTorch, y - 1, zTorch, support_block_id)  # Блок поддержки для факела из красного камня
        self.mc_mock.setBlock.assert_any_call(xTorch, y, zTorch, 76)  # Факел из красного камня на (xTorch, y, zTorch)

if __name__ == "__main__":
    unittest.main()
