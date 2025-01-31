# When creating an Agent, filename must be AGNT_className.py
from Framework.Utils.agent import Agent

class TemplateBot(Agent):

    def cmd_fake1(self, *args):
        """
        Command header
        """
        help_message = [
            "-> FAKE1 {ПАРАМЕТРЫ} Командин дийцар.",
            "* PARAMETER1: Параметрийн дийцар",
            "* PARAMETER2: Параметраш дӀаязъяр."
        ]
            
        actions = {
            "ЦААЛАР": self.default_mode, # кхочушдо NO параметраш хилча
            "ЛАМАСТ": self.custom_mode # кхочушдо нагахь санна параметр = ЛАМАСТ .
        }
        
        self.execute_cmd(help_message, actions, *args)

    def cmd_fake2(self, *args):
        """
        Командин корта .
        """
        help_message = [
            "-> FAKE2 ТӀедилларан дийцар."
        ]
            
        actions = {
            "ЦААЛАР": self.do_stuff, # кхочушдо NO параметраш хилча
        }
        
        self.execute_cmd(help_message, actions, *args)

    def default_mode(self, *args):
        """
        1-чу командан логика стандартан режиман .
        """
        # логика кхузахь (API кхайкхамаш)
        self.talk("Масал")

    def custom_mode(self, *args):
        """
        Къовсамийн режиман логика .
        """
        parameter = args[0] # масала
        result = self.method(parameter)
        # кхин а логика кхузахь (API кхайкхамаш)

    def do_stuff(Self, *args):
        """
        2-гӀа командан логика стандартан режиман .
        """
        parameter = args[0] # масала
        result = self.method(parameter)
        result = self.method2(result)
        # кхин а логика кхузахь (API кхайкхамаш)

    def method(self, parameter):
        """
        Цхьа хӀума деш, юхаверза йиш йолуш а, йиш йоцуш а.
        """
        # хӀума дан
        return result

    def method2(self, parameter):
        """
        Цхьа хӀума деш, юхаверза йиш йолуш а, йиш йоцуш а.
        """
        # кхин а алсам хӀуманаш де
        return result


