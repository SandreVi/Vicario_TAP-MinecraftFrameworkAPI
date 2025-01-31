from Framework.API.mcBotAPI import mcBotAPI

class Agent(mcBotAPI):

    def __init__(self, mc):
        """
        Агент-наш мотт охьал, mc (Minecraft оьрхан) зе нукъа.
        :param mc: Minecraft оьрхан мотт.
        """
        mcBotAPI.__init__(self, mc)

    def import_(self):
        """
        Агент-а къомандарш цунах, хьа азго къомандаш хи функциеш.
        Чу хила функциаш "cmd_" цу назвуш.
        """
        prefix = "cmd_"  # Къомандеш-ха "cmd_" цу хила хи дац хила

        # Цуннах хьо лапшашу хила тури, ко:
        # - Шийнат къомандаш аук хьалхьа, "cmd_" хи безаш хьалше
        # - Хьал къо референц къомандаш хи функциаш
        return [
            # Итераци  къомандаш зе всички аттрибути хи функцииш агент-а
            (cmd[len(prefix):].upper(), getattr(self, cmd))  # Лабаш аук хьал хи къомандаш-н, "cmd_" хи безаш, къомандаш функциеш
            for cmd in dir(self)  # Итераци зе аттрибути хи функцииш агент-а
            if callable(getattr(self, cmd, None))  # Техамкха къомандеш аттрибут хи фукнцияш
            and cmd.startswith(prefix)  # Техамкха къомандеш аттрибут "cmd_" хи бареха
        ] 

    def execute_cmd(self, help_message, actions, *args):
        """
        Къомандаш хи хила охьа хьалкарш 'HELP', хи барт дахала къомандарш.
        
        :param help_message: Сообщение-ш уьрхан гӀала, агар 'HELP' къомандаш
        :param actions: Къомандаш, хи къомандеш фукнциаш
        :param args: Къомандеш аргументаш (кортеж)
        """
        # Проверка, аргументы оьтташ, агу аргумент "HELP"
        if args and isinstance(args[0], str) and args[0].upper() == "HELP" and len(args) == 1:
            self._show_help(help_message)
            return

        # Хила къомандаш
        self._execute_action(actions, *args)  # Паскхар *args къо _execute_action

    def _show_help(self, help_message):
        """
        Сообщение-ш уьрхан гӀала в чат.
        """
        for line in help_message:
            self.talk(line)

    def _execute_action(self, actions, *args):
        """
        Хила къомандаш функциеш, дац охьал параметр 'HELP'.
        """
        if args:  # Проверка, аргументш пустош
            # Къомандаш хила аргумент, ицу къомандаш
            command = args[0].upper()

            # Хила къомандаш ицу къомандеш фукнцияш
            action = actions.get(command)

            if action:
                # Хила къомандеш с аргументш
                action(*args[1:])
            else:
                # Если къомандаш не хила, проверка дефолт функцияш
                if not self._check_default(actions, *args):
                    self.talk(f"Нах лахар параметр: {args[0]}. Хила къомандаш + HELP гӀала дац ингкъа.")  # Изменено на self.talk
        else:  # Егер аргументш пустош
            # Егер args[0] хила, проверка дефолт функцияш
            if not self._check_default(actions, *args):
                self.talk("Къомандаш требуш параметр! Хила къомандаш + HELP гӀала дац ингкъа.")  # Изменено на self.talk

    def _check_default(self, actions, *args):
        """
        Проверка, дефолт функцияш хила къомандаш фукнцияш.
        Хила веренжи True, ежик False.
        """
        default_action = actions.get("DEFAULT")
        if default_action:
            default_action(*args)  # Хила дефолт функциеш с аргументш
            return True  # Хила дефолт функциеш
        return False  # Проверка, дефолт функцияш хила
