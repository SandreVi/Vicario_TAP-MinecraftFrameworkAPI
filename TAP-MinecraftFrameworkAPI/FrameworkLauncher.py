from MyAdventures.mcpi.minecraft import Minecraft
from Framework.agent_manager import AgentManager

print('Фреймворк запущен')

# Соединение с сервером Minecraft
mc = Minecraft.create()

# Инстанцирование менеджера агентов
agent_manager = AgentManager(mc)

# Импорт всех агентов и отображение доступных къомандеш
agent_manager.start(False)

# Также можно запустить с автоматическим тайм-аутом -> agent_manager.start(True, timeoutInSeconds)

print('Фреймворк завершен')
