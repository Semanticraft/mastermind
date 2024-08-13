from abc import ABC, abstractmethod


class GuesserBot(ABC):
    """
    Interface for the GuesserBot
    """

    @abstractmethod
    def guess(self):
        """
        Guesses the secret code
        """
        pass

    @abstractmethod
    def obtain_feedback(self, black_pins, white_pins):
        """
        Obtains feedback from the game control
        """
        pass