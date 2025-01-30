import random
from Framework.Utils.agent import Agent

class ParrotBot(Agent):

    def cmd_insult(self, *args):
        """
        Method that gets executed when the "INSULT" command is received.
        """
        help_message = [
            "-> INSULT: The bot insults someone with a witty remark.",
            "-> INSULT CHECK {insult}: Checks if the insult is listed."
        ]
        
        actions = {
            "DEFAULT": self.just_insult,  # Call the default insult logic
            "CHECK": self.check_insult  # Call the check insult logic
        }

        self.execute_cmd(help_message, actions, *args)  # Pass *args

    def cmd_praise(self, *args):
        """
        Method that gets executed when the "PRAISE" command is received.
        """
        help_message = [
            "-> PRAISE: The bot praises someone with a nice compliment.",
            "-> PRAISE CHECK {praise}: Checks if the praise is listed."
        ]
        
        actions = {
            "DEFAULT": self.just_praise,  # Call the default praise logic
            "CHECK": self.check_praise  # Call the check praise logic
        }

        self.execute_cmd(help_message, actions, *args)  # Pass *args

    def cmd_mimic(self, *args):
        """
        Method that gets executed when the "MIMIC" command is received.
        """
        help_message = [
            "-> MIMIC {words}: The bot repeats the words you provide.",
            "Example: MIMIC Hello there!"
        ]
        
        actions = { 
            "DEFAULT": self.just_mimic  # Call the default mimic logic
        }

        self.execute_cmd(help_message, actions, *args)  # Pass *args

    def just_insult(self, *args):
        """
        Sends a random insult from a predefined list.
        """
        insults = self.get_insults()  # Get insults from the method
        insult = random.choice(insults)  # Choose one randomly from the list
        self.talk(insult)  # Use the talk() method from the API

    def just_praise(self, *args):
        """
        Sends a random compliment from a predefined list.
        """
        compliments = self.get_compliments()  # Get compliments from the method
        compliment = random.choice(compliments)  # Choose one randomly from the list
        self.talk(compliment)  # Use the talk() method from the API

    def just_mimic(self, *args):
        """
        Repeats the words provided by the user in the MIMIC command.
        """
        if args:
            self.talk(" ".join(args))  # Repeat the words that the player typed
        else:
            self.talk("I have nothing to mimic!")  # If no words were provided, respond with a default message

    def check_insult(self, *args):
        """
        Checks if the insult provided by the user is in the predefined list.
        """
        if args:
            insult = " ".join(args).upper()  # Convert the insult to uppercase
            insults = self.get_insults()  # Get insults
            self.check_word_in_list(insult, insults)  # Check if the word is in the list
        else:
            self.talk("Please provide an insult to check.")

    def check_praise(self, *args):
        """
        Checks if the compliment provided by the user is in the predefined list.
        """
        if args:
            compliment = " ".join(args).upper()  # Convert the compliment to uppercase
            compliments = self.get_compliments()  # Get compliments
            self.check_word_in_list(compliment, compliments)  # Check if the word is in the list
        else:
            self.talk("Please provide a compliment to check.")

    def check_word_in_list(self, word, word_list):
        """
        Common method to check if a word exists in the given list.
        """
        # Convert the list words to uppercase for case-insensitive comparison
        word_list_upper = list(map(lambda x: x.upper(), word_list))
        
        # Check if the word exists in the list
        if word in word_list_upper:
            self.talk(f"The word '{word}' is in the list! :)")  # If it's in the list
        else:
            self.talk(f"The word '{word}' is NOT in the list... :(")  # If it's not in the list

    def get_insults(self):
        """
        Returns the list of predefined insults with proper capitalization.
        """
        return [
            "Fool",
            "Idiot",
            "Imbecile",
            "Moron",
            "Donkey",
            "Jerk",
            "Stupid"
        ]

    def get_compliments(self):
        """
        Returns the list of predefined compliments with proper capitalization.
        """
        return [
            "Awesome",
            "Incredible",
            "Brilliant",
            "Outstanding",
            "Fantastic",
            "Smart",
            "Talented",
            "Genius",
            "Amazing",
            "Sharp"
        ]
