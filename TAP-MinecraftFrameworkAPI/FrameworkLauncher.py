# FrameworkLauncher.py
from MyAdventures.mcpi.minecraft import Minecraft
from Framework.agent_manager import AgentManager

print('Framework launched')

# Connect to the Minecraft server
mc = Minecraft.create()

# Create an instance of the AgentManager
agent_manager = AgentManager(mc)

# Import all agents and show their available commands
agent_manager.start(False)

# It can also be launched with automatic timeout -> agent_manager.start(True, timeoutInSeconds)

print('Framework stopped')
