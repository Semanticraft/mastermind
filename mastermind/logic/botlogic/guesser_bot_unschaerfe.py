import numpy as np

from mastermind.logic.botlogic.guesser_bot_least_worst_case import GuesserBotLeastWorstCase


def log_to_file(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")


class GuesserBotUnschaerfe(GuesserBotLeastWorstCase):

    def __init__(self, sequence_length, color_count, fuzziness_level=0.1):
        """
        Initializes the fuzzy bot with an additional fuzziness level.

        :param sequence_length: The length of the code sequence.
        :param color_count: The number of possible colors.
        :param fuzziness_level: The probability of making a fuzzy guess.
        """
        super().__init__(sequence_length, color_count)
        self.fuzziness_level = fuzziness_level
        self.__guess_count = 0
        self.__rand_value = 1

    def reset_lists(self, sequence_length, color_count):
        """
        Resets the lists of possible codes and the guess count.
        """
        self.__guess_count = 0
        super().reset_lists(sequence_length, color_count)

    def guess(self):
        """
        Takes a guess based on the least amount of worst-case scenarios, but with some fuzziness.
        """

        self.__rand_value = np.random.random()
        if self._most_recent_guess is None:
            self._most_recent_guess = self.take_first_guess()
        else:
            if self.__rand_value < self.fuzziness_level:
                # Make a fuzzy guess by selecting a random code from the remaining codes
                self._most_recent_guess = np.random.choice(self._remaining_codes)
            else:
                self._most_recent_guess = min(self._remaining_codes, key=self._calculate_worst_case)

        self.__guess_count += 1
        return self._most_recent_guess

    def obtain_feedback(self, black_pins, white_pins):
        """
        Updates the remaining codes based on the feedback by discarding codes that are not possible anymore,
        but with some fuzziness in the process.
        """

        self._remaining_codes.remove(self._most_recent_guess)  # Remove the most recent guess

        # only discarding codes if the feedback is not too fuzzy
        if (self.__guess_count < 2) or (self.__rand_value > self.fuzziness_level):
            self._discard_by_overlap(black_pins)
            self._discard_by_number(black_pins + white_pins)

        self._remaining_code_sets = [set(code) for code in self._remaining_codes]
