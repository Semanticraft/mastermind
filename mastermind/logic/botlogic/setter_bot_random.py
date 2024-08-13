from .setter_bot_interface import SetterBot
from random import randrange


class RandomSetterBot(SetterBot):
    """
    RandomSetterBot class that implements the SetterBot interface and sets the code randomly.
    """

    def set_code(self, sequence_length, color_count):
        code_str = ""
        for i in range(sequence_length):
            code_str += randrange(1, color_count + 1).__str__()
        return int(code_str)
