from abc import ABC, abstractmethod


class SetterBot(ABC):
    """
    Interface for the SetterBot
    """

    @abstractmethod
    def set_code(self, sequence_length, color_count):
        """
        Sets the secret code for the game
        """
        pass
