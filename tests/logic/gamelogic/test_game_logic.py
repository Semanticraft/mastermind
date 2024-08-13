import unittest

from mastermind.logic.gamelogic.game_logic import evaluate


class TestGameLogicMethods(unittest.TestCase):

    def checkEvaluation(self, guess: int, actual_code: int, black_pins: int, white_pins: int) -> None:
        turn = evaluate(guess, actual_code)
        self.assertTrue(turn.black_pins == black_pins and turn.white_pins == white_pins)

    def test_limits(self):
        """Method to test limits of black and white pins to be returned for different code lengths."""
        self.checkEvaluation(11111, 11111, 5, 0)
        self.checkEvaluation(88888, 88888, 5, 0)
        self.checkEvaluation(88888, 11111, 0, 0)
        self.checkEvaluation(11111, 88888, 0, 0)
        self.checkEvaluation(12435, 54321, 0, 5)
        self.checkEvaluation(54231, 12345, 0, 5)
        self.checkEvaluation(1111, 1111, 4, 0)
        self.checkEvaluation(8888, 8888, 4, 0)
        self.checkEvaluation(8888, 1111, 0, 0)
        self.checkEvaluation(1111, 8888, 0, 0)
        self.checkEvaluation(1234, 4321, 0, 4)
        self.checkEvaluation(4321, 1234, 0, 4)

    def test_black_pins_vs_white_pins(self):
        """Method to test combinations of black and white pins that should be returned."""
        self.checkEvaluation(1552, 1234, 1, 1)
        self.checkEvaluation(1325, 1234, 1, 2)
        self.checkEvaluation(1423, 1234, 1, 3)
        self.checkEvaluation(15432, 12345, 1, 4)
        self.checkEvaluation(1245, 1234, 2, 1)
        self.checkEvaluation(1243, 1234, 2, 2)
        self.checkEvaluation(12534, 12345, 2, 3)
        self.checkEvaluation(12351, 12345, 3, 1)
        self.checkEvaluation(12354, 12345, 3, 2)

    def test_black_pins_at_end_of_guess(self):
        """Method to test what happens, if white pins should be given at the beginning and black pins at the end."""
        self.checkEvaluation(1234, 2134, 2, 2)

    def test_repeating_colors(self):
        """Method to test, if the correct pins are returned when using repeating but different colors for guess and
        actual code, respectively.
        """
        self.checkEvaluation(2323, 3123, 2, 1)
        self.checkEvaluation(2323, 3222, 1, 2)
        self.checkEvaluation(2333, 3212, 0, 2)
        self.checkEvaluation(23235, 12355, 1, 2)
        self.checkEvaluation(23334, 32221, 0, 2)
        self.checkEvaluation(23232, 32222, 2, 2)
        self.checkEvaluation(22223, 32221, 3, 1)


if __name__ == '__main__':
    unittest.main()
