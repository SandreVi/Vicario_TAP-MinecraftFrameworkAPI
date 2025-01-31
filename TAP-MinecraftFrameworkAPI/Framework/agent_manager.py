import time
import importlib
import os
import inspect
from Framework.Utils.chat_listener import ChatListener

class AgentManager(ChatListener):
    def __init__(self, mc):
        """
        Агент менеджер хила, со агентш тӀекъах чо чат къомандеш хила.
        :param mc: Minecraft соединение.
        """
        super().__init__(mc)
        self.agents = {}  # Агентш хила, агент хьама а ща класса
        self.commands = {}  # Къомандеш хила, къоманда хьама метод

    def import_agents(self):
        """
        Динамическ импорт агентш 'Agents' цу и регистрация хила къомандеш.
        """
        # Путь, со агентш файлаш
        agents_path = os.path.join(os.path.dirname(__file__), 'Agents')
        
        # Листена агентш файлшу хила фильтра, со къомандеш начинается "AGNT_" и заканчивается ".py"
        agent_files = filter(lambda filename: filename.startswith("AGNT_") and filename.endswith(".py"), os.listdir(agents_path))

        # Лахан каждый правильный агент файл
        for filename in agent_files:
            agent_name = filename[:-3]  # Мы удаляем '.py' расширение для класса хьам
            agent_module = importlib.import_module(f"Framework.Agents.{agent_name}")
            
            # Динамически берет класс из модуля (КЛАСС ХЬАМА СОШЕН СУФФИКСОМ ФАЙЛА)
            class_name = agent_name.split("_")[1]  # Класс хьама после "AGNT_"
            try:
                agent_class = getattr(agent_module, class_name)  # Получить класс из модуля
            except AttributeError:
                print(f"Ошибка: Модуль {agent_name} не имеет класса с именем {class_name}.")
                continue
            
            # Агент инстанцирования
            agent_instance = agent_class(self.mc)  # Инстанцировать агент
            
            # Вызвать метод импорт агента для регистрации къомандеш
            agent_commands = agent_instance.import_()
            
            # Регистрация къомандеш и методов
            for command, method in agent_commands:
                self.commands[command] = method  # Сопоставить къомандеш к методу
            
            # Сохранить агент инстанцирование
            self.agents[agent_name] = agent_instance

    def process_message(self, command):
        """
        Процесс чо къомандеш хила, если он допустим.
        """
        if command is None:
            self.mc.postToChat("Слишком много времени бездействия... Фреймворк закрывается!")
            return

        # Разделить къомандеш в части и убрать пробелы
        parts = command.split()  # Это разделяет къомандеш и параметры правильно
        command = parts[0].upper()  # Преобразовать къомандеш к верхнему регистру для согласованности
        params = parts[1:]  # Получить параметры, кроме къомандеш

        # Словарь для обработки къомандеш
        command_actions = {
            "CMDLIST": lambda: self.mc.postToChat("Доступные къомандеш: " + ", ".join(self.commands.keys())),
            "COMMANDLIST": lambda: self.mc.postToChat("Доступные къомандеш: " + ", ".join(self.commands.keys())),
            "HELP": lambda: [
                self.mc.postToChat("->CMDLIST/COMMANDLIST: Показать доступные къомандеш для агентш"),
                self.mc.postToChat("->RELOAD: Обновить загруженные агентш из папки Agents"),
                self.mc.postToChat("->END/STOP: Закрыть фреймворк"),
                self.mc.postToChat("->HELP: Этот къомандеш! (само объясняющийся)")
            ],
            "RELOAD": lambda: [
                self.agents.clear(),
                self.commands.clear(),
                self.import_agents(),
                self.mc.postToChat("Агенты обновлены!")
            ],
            "END": lambda: self.mc.postToChat("Для корректного завершения, просто напиши \"END\" или \"STOP\" без дополнительных параметров"),
            "STOP": lambda: self.mc.postToChat("Для корректного завершения, просто напиши \"END\" или \"STOP\" без дополнительных параметров")
        }

        # Случай по умолчанию для къомандеш агента
        if command in command_actions:
            command_actions[command]()  # Выполнить соответствующее действие
        elif command in self.commands:
            method = self.commands[command]
            method(*params)
        else:
            self.mc.postToChat(f"Къомандеш '{command}' не распознан.")

    def start(self, timeout_enabled=True, timeout=10):
        """
        Инициализирует менеджер агентш, импортирует агентш и начинает слушать къомандеш из чата.
        """
        # Импорт агентш и их къомандеш
        self.import_agents()

        self.mc.postToChat("Агенты импортированы! Слушаем...")
        self.mc.postToChat("Напиши \"HELP\", если нужно!")

        # Начать слушать къомандеш из чата
        self.listen_for_chat_commands(self, timeout_enabled, timeout)  # Вызвать метод listen_for_chat_commands из ChatListener

        # Прощальное сообщение
        self.mc.postToChat("Фреймворк закрыт!")
