import unittest
from unittest.mock import patch
import numpy as np
from mastermind.logic.botlogic.guesser_bot_unschaerfe import GuesserBotUnschaerfe


class TestGuesserBotUnschaerfe(unittest.TestCase):

    def setUp(self):
        self.bot = GuesserBotUnschaerfe(sequence_length=4, color_count=6, fuzziness_level=0.1)

    @patch('numpy.random.random')
    @patch('numpy.random.choice')
    def test_happy_path(self, mock_choice, mock_random):
        mock_random.return_value = 0.2  # No fuzziness
        mock_choice.return_value = '1122'  # Mock choice in case of fuzziness
        guess = self.bot.guess()
        self.assertIsNotNone(guess)
        self.assertTrue(len(guess) == 4)

    @patch('numpy.random.random')
    def test_worst_case(self, mock_random):
        mock_random.return_value = 0.9  # High chance of non-fuzziness
        self.bot.guess()  # Initial guess
        self.bot.obtain_feedback(0, 0)  # Worst feedback
        second_guess = self.bot.guess()
        self.assertIsNotNone(second_guess)
        self.assertTrue(len(second_guess) == 4)

    @patch('numpy.random.random')
    def test_average_case(self, mock_random):
        mock_random.side_effect = [0.5, 0.2, 0.8]  # Varying randomness
        self.bot.guess()
        self.bot.obtain_feedback(1, 1)
        second_guess = self.bot.guess()
        self.assertIsNotNone(second_guess)
        self.assertTrue(len(second_guess) == 4)

    @patch('numpy.random.random')
    def test_fuzziness_impact(self, mock_random):
        mock_random.return_value = 0.05  # Force fuzziness
        guess = self.bot.guess()
        self.assertIsNotNone(guess)
        self.assertTrue(len(guess) == 4)

    def test_feedback_handling(self):
        self.bot.guess()
        self.bot.obtain_feedback(2, 2)  # Specific feedback
        self.assertTrue(len(self.bot._remaining_codes) < len(self.bot._all_possible_codes))


if __name__ == '__main__':
    unittest.main()
