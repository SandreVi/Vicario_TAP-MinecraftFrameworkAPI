import random
from Framework.Utils.agent import Agent

class ParrotBot(Agent):

    def cmd_insult(self, *args):
        """
        "INSULT" команда схьаэцча кхочушъеш йолу метод.
        """
        help_message = [
            "-> INSULT: Бот цхьанна вас йо забаречу къамелца.",
            "-> INSULT ТОЛЛАМ {insult}: Инсульт листа йина юй толлу."
        ]
        
        actions = {
            "DEFAULT": self.just_insult,  # Кхайкха стандартан инсульт логика .
            "CHECK": self.check_insult  # Кхайкхам чекхбаккха оскорбление логика .
        }

        self.execute_cmd(help_message, actions, *args)  # Чекхдала *args

    def cmd_praise(self, *args):
        """
        "PRAISE" команда схьаэцча кхочушъеш йолу метод.
        """
        help_message = [
            "-> PRAISE: Бот цхьаъ хеставо хаза комплиментца.",
            "-> PRAISE ТОЛЛАМ {praise}: Хастам листа бу я бац толлу."
        ]
        
        actions = {
            "DEFAULT": self.just_praise,  # Кхайкха стандартан хастаман логика .
            "CHECK": self.check_praise  # Кхайкхам чекхбаккха хастаме логика .
        }

        self.execute_cmd(help_message, actions, *args)  # Pass *args

    def cmd_mimic(self, *args):
        """
        "MIMIC" команда схьаэцча кхочушъеш йолу метод
        """
        help_message = [
            "-> MIMIC {words}: Бот ахь луш долу дешнаш карладохуш ду.",
            "Масала: MIMIC Салам маршал ду шуьга"
        ]
        
        actions = { 
            "DEFAULT": self.just_mimic  # Кхайкха стандартан мимика логика .
        }

        self.execute_cmd(help_message, actions, *args)  # Чекхдала *args

    def just_insult(self, *args):
        """
        Хьалха билгалдаьккхинчу тептар тӀера ларамаза вас йоуьйту.
        """
        insults = self.get_insults()  # Методах оскорблени эца .
        insult = random.choice(insults)  # Цхьаъ ларамаза харжа тептар тӀера .
        self.talk(insult)  # API чуьра talk() метод лелае .

    def just_praise(self, *args):
        """
        Хьалха билгалдаьккхинчу тептар тӀера ларамаза комплимент йоуьйту.
        """
        compliments = self.get_compliments()  # Методан комплименташ эца .
        compliment = random.choice(compliments)  # Цхьаъ ларамаза харжа тептар тӀера .
        self.talk(compliment)  # API чуьра talk() метод лелае .

    def just_mimic(self, *args):
        """
        MIMIC командехь лелочо делла дешнаш карладоху.
        """
        if args:
            self.talk(" ".join(args))  # Ловзаргахь дӀаяздина дешнаш карладаха .
        else:
            self.talk("Суна имитаци ян хӀума дац!")  # Нагахь санна цхьа а дешнаш ца делча, хьалха санна хаамца жоп ло

    def check_insult(self, *args):
        """
        Декъашхочо елла вас хьалххе билгалдаьккхинчу тептарехь юй толлу.
        """
        if args:
            insult = " ".join(args).upper()  # Вас деш долу дешнаш доккхачу элпаца дерзаде .
            insults = self.get_insults()  # Вас еш.
            self.check_word_in_list(insult, insults)  # Дош тептар тӀехь дуй хьовса .
        else:
            self.talk("Please provide an insult to check.")

    def check_praise(self, *args):
        """
        Декъашхочо елла комплимент хьалххе билгалдаьккхинчу тептарехь юй толлу.
        """
        if args:
            compliment = " ".join(args).upper()  # Комплимент доккхачу элпаца хийца .
            compliments = self.get_compliments()  # Комплименташ эца .
            self.check_word_in_list(compliment, compliments)  # Дош тептар тӀехь дуй хьовса .
        else:
            self.talk("Комплимент язъе, хьажа.")

    def check_word_in_list(self, word, word_list):
        """
        Деллачу тептарехь дош дуйла толлуш юкъара кеп.
        """
        # Список дешнаш доккхачу элпе дерзаде, доккхачу элпаца дустар дан
        word_list_upper = list(map(lambda x: x.upper(), word_list))
        
        # Списокехь дош дуй хьовса .
        if word in word_list_upper:
            self.talk(f"'{word}' боху дош листа чохь ду! :)")  # Нагахь санна иза списокехь делахь
        else:
            self.talk(f"'{word}' боху дош цу тептарехь ДАЦ... :(")  # Нагахь санна иза списокехь дацахь

    def get_insults(self):
        """
        Хьалха билгалдаьхначу васийн тептар юхадерзадо, нийса доккха элп а яздина.
        """
        return [
            "Ӏовдал",
            "Идиот",
            "Имбецил",
            "Морон",
            "Вир",
            "Ӏовдал",
            "Ӏовдал"
        ]

    def get_compliments(self):
        """
        Хьалха билгалдаьхначу комплиментийн тептар юхадерзадо, нийса доккха элп а яздина.
        """
        return [
            "Инзаре",
            "Тамаше",
            "Къега",
            "ГӀараваьлла",
            "Фантастическан",
            "Хьекъале",
            "ПохӀма долу",
            "Гени",
            "Тамаше",
            "Ира"
        ]
