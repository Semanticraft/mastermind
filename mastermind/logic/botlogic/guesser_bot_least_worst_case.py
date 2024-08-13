from collections import Counter

import numpy as np

from mastermind.logic.botlogic.guesser_bot_interface import GuesserBot

numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
doubles = ["11", "22", "33", "44", "55", "66", "77", "88"]


def log_to_file(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")


def calculate_overlap(code1, code2):
    """
    Calculates how many numbers are exactly the same and in the same position in both codes.
    """
    return sum(c1 == c2 for c1, c2 in zip(code1, code2))


def calculate_resemblance(code1, code2):
    """
    Calculates how many numbers are the same in both codes not considering their position.
    """
    return len(list((Counter(code1) & Counter(code2)).elements()))


class GuesserBotLeastWorstCase(GuesserBot):

    def __init__(self, sequence_length, color_count):
        self._most_recent_guess = None

        self._sequence_length = None
        self._color_count = None

        self._all_possible_codes = None
        self._remaining_codes = None
        self._remaining_code_sets = None

        self.reset_lists(sequence_length, color_count)

    @property
    def remaining_codes(self):
        return self._remaining_codes

    def reset_lists(self, sequence_length, color_count):

        self._most_recent_guess = None

        self._sequence_length = sequence_length
        self._color_count = color_count

        self._all_possible_codes = self.__generate_codes_list(sequence_length, color_count)

        self._remaining_codes = self._all_possible_codes.copy()
        self._remaining_code_sets = [set(code) for code in self._remaining_codes]

        np.random.shuffle(self._remaining_codes)

    def __generate_codes_list(self, sequence_length, color_count, prefix=""):
        """
        Generates a list of all possible codes
        """
        if sequence_length == 0:
            return [prefix]
        else:
            result = []
            for number in numbers[:color_count]:
                result += self.__generate_codes_list(sequence_length - 1, color_count, prefix + number)
            return result

    def guess(self):
        """
        Takes a guess based on the least amount of worst case scenarios
        """
        # calculating first guess by worst case method is incredibly slow and inefficient. Tried this instead.
        if self._most_recent_guess is None:
            self._most_recent_guess = self.take_first_guess()
        else:
            self._most_recent_guess = min(self._remaining_codes, key=self._calculate_worst_case)

        return self._most_recent_guess

    def take_first_guess(self):

        guess = ""

        if self._sequence_length == 4:
            first = numbers[np.random.randint(0, self._color_count)]
            remaining_numbers = numbers.copy()
            remaining_numbers.remove(first)
            second = remaining_numbers[np.random.randint(0, self._color_count - 1)]
            guess = first + first + second + second

        elif self._sequence_length == 5:
            first = numbers[np.random.randint(0, self._color_count)]
            remaining_numbers = numbers.copy()
            remaining_numbers.remove(first)
            second = remaining_numbers[np.random.randint(0, self._color_count - 1)]
            if self._color_count > 2:
                remaining_numbers.remove(second)
            limit = self._color_count - 2 if self._color_count > 2 else self._color_count - 1
            third = remaining_numbers[np.random.randint(0, limit)]
            guess = first + first + second + second + third

        return guess

    def _calculate_worst_case(self, code):
        """
        Calculates how many possible code would remain if the feedback was neither a black nor a white peg
        """
        guess_numbers = set(code)

        return sum(1 for code_set in self._remaining_code_sets if guess_numbers.isdisjoint(code_set))

    def obtain_feedback(self, black_pins, white_pins):
        """
        Updates the remaining codes based on the feedback by discarding codes that are not possible anymore.
        """

        self._remaining_codes.remove(self._most_recent_guess)  # remove the most recent guess
        self._discard_by_overlap(black_pins)
        self._discard_by_number(black_pins + white_pins)
        self._remaining_code_sets = [set(code) for code in self._remaining_codes]

    def _discard_by_overlap(self, black_pins):
        """
        Discard codes that don't have the exact overlap with the most recent guess.

        Example:
        --------
        With a guess of 4233 and a feedback of 2 black pins, all remaining codes would require
        exactly two of the guesses numbers in the same position.
        """
        self._remaining_codes = [code for code in self._remaining_codes
                                 if calculate_overlap(code, self._most_recent_guess) == black_pins]

    def _discard_by_number(self, amount):
        """
        Discards all codes that don't have at least n of the recent guesses colors in them.
        Where n is the amount of black and white pins.
        """
        self._remaining_codes = [code for code in self._remaining_codes
                                 if calculate_resemblance(self._most_recent_guess, code) == amount]
