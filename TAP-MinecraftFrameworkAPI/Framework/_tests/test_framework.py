import unittest
from unittest.mock import MagicMock
from Framework.Utils.chat_listener import ChatListener
from Framework.agent_manager import AgentManager


class TestAgentManager(unittest.TestCase):

    def setUp(self):
        self.mc_mock = MagicMock()
        self.agent_manager = AgentManager(self.mc_mock)

    def test_import_agents(self):
        # Test importing agents from the Agents folder
        self.agent_manager.import_agents()

        # If there are agents, ensure the agents and commands dictionaries are not empty
        if self.agent_manager.agents:
            self.assertGreater(len(self.agent_manager.agents), 0)
            self.assertGreater(len(self.agent_manager.commands), 0)
        else:
            # If no agents are present, check that both dictionaries are empty
            self.assertEqual(len(self.agent_manager.agents), 0)
            self.assertEqual(len(self.agent_manager.commands), 0)

    def test_process_message_valid_command(self):
        # Test processing a valid command
        self.agent_manager.commands = {"TESTCOMMAND": MagicMock()}  # Mock the "TESTCOMMAND" method
        self.agent_manager.process_message("TESTCOMMAND param1 param2")  # Process the command with parameters
        self.agent_manager.commands["TESTCOMMAND"].assert_called_with("param1", "param2")  # Check that the command was called with correct params
        self.mc_mock.postToChat.assert_not_called()  # Ensure no message was posted to chat

    def test_process_message_invalid_command(self):
        # Test processing an invalid command
        self.agent_manager.process_message("INVALIDCOMMAND")  # Process a command that doesn't exist
        self.mc_mock.postToChat.assert_called_with("Command 'INVALIDCOMMAND' not recognized.")  # Ensure the correct message is posted to chat

    def test_process_message_help(self):
        # Test the help command
        self.agent_manager.process_message("HELP")  # Process the "HELP" command
        # Check if the help message contains the expected text
        self.assertTrue(any("->CMDLIST/COMMANDLIST: Show available commands for agents" in args[0] for args in self.mc_mock.postToChat.call_args_list))
        
    def test_process_message_reload(self):
        # Test the RELOAD command
        self.agent_manager.import_agents = MagicMock()  # Mock the import_agents method to avoid actual file operations
        self.agent_manager.process_message("RELOAD")  # Process the "RELOAD" command
        self.agent_manager.import_agents.assert_called_once()  # Ensure that import_agents is called
        self.mc_mock.postToChat.assert_called_with("Agents reloaded!")  # Ensure the reload message is posted to chat
        
    def test_process_message_stop(self):
        # Test the STOP command
        self.agent_manager.process_message("STOP")  # Process the "STOP" command
        self.mc_mock.postToChat.assert_called_with("To properly abort, JUST type \"END\" or \"STOP\" with no extra parameters")  # Notify the STOP command must be posted with NO extra parameters

    def test_process_message_stop(self):
        # Test the END command
        self.agent_manager.process_message("STOP")  # Process the "END" command
        self.mc_mock.postToChat.assert_called_with("To properly abort, JUST type \"END\" or \"STOP\" with no extra parameters")  # Notify the END command must be posted with NO extra parameters

