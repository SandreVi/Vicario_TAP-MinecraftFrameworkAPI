# When creating an Agent, filename must be AGNT_className.py
from Framework.Utils.agent import Agent

class TemplateBot(Agent):

    def cmd_fake1(self, *args):
        """
        Command header
        """
        help_message = [
            "-> FAKE1 {PARAMETERS} Command description.",
            "* PARAMETER1: Parameter description.",
            "* PARAMETER2: Parameter description."
        ]
            
        actions = {
            "DEFAULT": self.default_mode, # executed when NO parameters
            "CUSTOM": self.custom_mode # executed if parameter = CUSTOM
        }
        
        self.execute_cmd(help_message, actions, *args)

    def cmd_fake2(self, *args):
        """
        Command header
        """
        help_message = [
            "-> FAKE2 Command description."
        ]
            
        actions = {
            "DEFAULT": self.do_stuff, # executed when NO parameters
        }
        
        self.execute_cmd(help_message, actions, *args)

    def default_mode(self, *args):
        """
        Default mode logic for command 1
        """
        # logic here (API calls)
        self.talk("Example")

    def custom_mode(self, *args):
        """
        Custom mode logic
        """
        parameter = args[0] # for example
        result = self.method(parameter)
        # more logic here (API calls)

    def do_stuff(Self, *args):
        """
        Default mode logic for command 2
        """
        parameter = args[0] # for example
        result = self.method(parameter)
        result = self.method2(result)
        # more logic here (API calls)

    def method(self, parameter):
        """
        Does something and can or cannot return.
        """
        # do stuff
        return result

    def method2(self, parameter):
        """
        Does something and can or cannot return.
        """
        # do even more stuff
        return result


