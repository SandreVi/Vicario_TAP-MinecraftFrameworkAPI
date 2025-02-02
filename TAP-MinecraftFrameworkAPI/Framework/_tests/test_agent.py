import unittest
from unittest.mock import MagicMock
from Framework.API.mcBotAPI import mcBotAPI
from Framework.Utils.agent import Agent

class TestAgent(unittest.TestCase):

    def setUp(self):
        self.mock_mc = MagicMock()
        self.agent = Agent(self.mock_mc)

    def test_import_commands(self):
        # Add a simulated command 'cmd_fake_command'
        def cmd_fake_command(self):
            return "This is a fake command"

        self.agent.cmd_fake_command = cmd_fake_command

        commands = self.agent.import_()

        # Verify that the command has been imported correctly
        self.assertEqual(len(commands), 1)  # There should be 1 command
        self.assertEqual(commands[0][0], "FAKE_COMMAND")  # The command name should be 'FAKE_COMMAND'
        self.assertEqual(commands[0][1], cmd_fake_command)  # The associated method should be 'cmd_fake_command'

    def test_execute_cmd_help(self):
        # Create a simulated help message
        help_message = ["->FAKE_COMMAND: executes a fake command with a fake funcionality."]
        
        # Create a simulated actions dictionary
        actions = {
            "FAKE_COMMAND": lambda: "Executed fake command"
        }

        # Execute the command with the HELP argument
        self.agent.execute_cmd(help_message, actions, "HELP")

        # Verify that the help message has been sent
        self.agent._show_help = MagicMock()
        self.agent.execute_cmd(help_message, actions, "HELP")
        self.agent._show_help.assert_called_once_with(help_message)

    def test_execute_cmd_action(self):
        # Create a simulated actions dictionary
        actions = {
            "FAKE_COMMAND": MagicMock() # We mock the action attached to the command
        }

        # Execute the command
        self.agent.execute_cmd([], actions, "FAKE_COMMAND", "arg1", "arg2")

        # Verify that the command's action was executed
        actions["FAKE_COMMAND"].assert_called_once_with("arg1", "arg2")

    def test_execute_cmd_invalid_action(self):
        # Create a simulated actions dictionary
        actions = {}

        self.agent.talk = MagicMock()

        # Execute an invalid command
        self.agent.execute_cmd([], actions, "INVALID_PARAMETER")

        # Verify that the agent talked about the invalid command
        self.agent.talk.assert_called_once_with("Invalid parameter: INVALID_PARAMETER. Use command + HELP for available options.")

    def test_execute_cmd_default_action(self):
        # Create a simulated actions dictionary with a default action
        actions = {
            "DEFAULT": MagicMock()
        }

        # Execute a command without parameters
        self.agent.execute_cmd([], actions)

        # Verify that the default action was called
        actions["DEFAULT"].assert_called_once()
