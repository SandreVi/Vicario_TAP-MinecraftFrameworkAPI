import unittest
from unittest.mock import MagicMock
from Framework.API.mcBotAPI import mcBotAPI
from MyAdventures.mcpi.vec3 import Vec3

class TestMcBotAPI(unittest.TestCase):

    # I've only made tests that check the functionality of the API

    def setUp(self):
        self.mc_mock = MagicMock()

        self.bot_api = mcBotAPI(self.mc_mock)

    def test_talk(self):
        # Test the talk method to check if the message is sent to the Minecraft chat
        message = "Hello, Minecraft!"
        self.bot_api.talk(message)
        self.mc_mock.postToChat.assert_called_with(message)

    def test_move(self):
        # Test the move method to ensure that the player's position is set correctly
        x, y, z = 10, 20, 30
        self.bot_api.move(x, y, z)
        self.mc_mock.player.setTilePos.assert_called_with(Vec3(x, y, z))

    def test_where(self):
        # Test the where method to ensure the current position of the player is returned correctly
        self.mc_mock.player.getTilePos.return_value = Vec3(10, 20, 30)
        x, y, z = self.bot_api.where()
        self.assertEqual((x, y, z), (10, 20, 30))

    def test_get_player_orientation(self):
        # Test the get_player_orientation method to ensure it returns the correct direction
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
        # Test the arrange_positions method to ensure it generates positions around the player
        self.mc_mock.player.getTilePos.return_value = Vec3(10, 20, 30)
        self.bot_api.where = MagicMock(return_value=(10, 20, 30))

        positions = self.bot_api.arrange_positions()
        
        # Verify that the positions generated are within the expected range
        self.assertEqual(len(positions), 3)
        self.assertTrue(all(isinstance(pos, tuple) and len(pos) == 3 for pos in positions))

    def test_calculate_position_north(self):
        # Test the calculate_position method for NORTH
        x, z, y = 10, 20, 30
        rotation = "NORTH"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        self.assertEqual(x, 10)  # x stays the same for NORTH
        self.assertEqual(z, 15)  # z decreases by block_distance (5) for NORTH
        self.assertEqual(y, 30)  # y stays the same
        self.assertEqual(xTorch, 10)  # Redstone torch x position
        self.assertEqual(zTorch, 14)  # Redstone torch z position = z - 1

    def test_calculate_position_east(self):
        # Test the calculate_position method for EAST
        x, z, y = 10, 20, 30
        rotation = "EAST"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        # Assert the correct final position based on the rotation and redstone torch addition
        self.assertEqual(x, 15)  # x increases by block_distance (5) for EAST
        self.assertEqual(z, 20)  # z stays the same
        self.assertEqual(y, 30)  # y stays the same
        self.assertEqual(xTorch, 16)  # Redstone torch x position = x + 1
        self.assertEqual(zTorch, 20)  # Redstone torch z position

    def test_calculate_position_south(self):
        # Test the calculate_position method for SOUTH
        x, z, y = 10, 20, 30
        rotation = "SOUTH"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        # Assert the correct final position based on the rotation and redstone torch addition
        self.assertEqual(x, 10)  # x stays the same
        self.assertEqual(z, 25)  # z increases by block_distance (5) for SOUTH
        self.assertEqual(y, 30)  # y stays the same
        self.assertEqual(xTorch, 10)  # Redstone torch x position
        self.assertEqual(zTorch, 26)  # Redstone torch z position = z + 1

    def test_calculate_position_west(self):
        # Test the calculate_position method for WEST
        x, z, y = 10, 20, 30
        rotation = "WEST"
        add_redstone = True
        x, z, y, xTorch, zTorch = self.bot_api.calculate_position(x, z, y, rotation, add_redstone)

        # Assert the correct final position based on the rotation and redstone torch addition
        self.assertEqual(x, 5)  # x decreases by block_distance (5) for WEST
        self.assertEqual(z, 20)  # z stays the same
        self.assertEqual(y, 30)  # y stays the same
        self.assertEqual(xTorch, 4)  # Redstone torch x position = x - 1
        self.assertEqual(zTorch, 20)  # Redstone torch z position

    def test_place_block(self):
        # Test the place_block method to verify that blocks are placed correctly
        x, z, y = 10, 20, 30
        xTorch, zTorch = 11, 20
        block_id = 1
        support_block_id = 4
        add_redstone = True
        activate_on_place = False

        # Call place_block method
        self.bot_api.place_block(x, z, y, xTorch, zTorch, block_id, add_redstone, support_block_id, activate_on_place)

        # Assert that the Minecraft API methods were called to set the blocks
        self.mc_mock.setBlock.assert_any_call(x, y - 1, z, support_block_id)  # Support block at (x, y-1, z)
        self.mc_mock.setBlock.assert_any_call(x, y, z, block_id, 0)  # Main block at (x, y, z) with no activation
        self.mc_mock.setBlock.assert_any_call(xTorch, y - 1, zTorch, support_block_id)  # Support block for redstone torch
        self.mc_mock.setBlock.assert_any_call(xTorch, y, zTorch, 76)  # Redstone torch at (xTorch, y, zTorch)
        
    def test_place_block_with_activation(self):
        # Test the place_block method with manual activation (activate_on_place=True)
        x, z, y = 10, 20, 30
        xTorch, zTorch = 11, 20
        block_id = 1
        support_block_id = 4
        add_redstone = True
        activate_on_place = True  # Enable manual activation

        # Call place_block method
        self.bot_api.place_block(x, z, y, xTorch, zTorch, block_id, add_redstone, support_block_id, activate_on_place)

        # Assert that the Minecraft API methods were called to set the blocks
        self.mc_mock.setBlock.assert_any_call(x, y - 1, z, support_block_id)  # Support block at (x, y-1, z)
        self.mc_mock.setBlock.assert_any_call(x, y, z, block_id, 1)  # Main block at (x, y, z) with activation (1)
        self.mc_mock.setBlock.assert_any_call(xTorch, y - 1, zTorch, support_block_id)  # Support block for redstone torch
        self.mc_mock.setBlock.assert_any_call(xTorch, y, zTorch, 76)  # Redstone torch at (xTorch, y, zTorch)

if __name__ == "__main__":
    unittest.main()
