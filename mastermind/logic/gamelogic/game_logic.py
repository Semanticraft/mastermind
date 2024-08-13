from typing import Tuple, Any

from .turn import Turn


# These are methods for running the game, which are used in the GameControl class

def validate(code: int, sequence_length: int, color_count: int) -> bool:
    """
    Checks if code has length of sequence_length and doesn't contain colors, which are not specified by color_count.

    Parameters
    ----------
    code: code to be checked
    sequence_length: length of te code
    color_count: number of different colors. code shouldn't have digits greater than this number
    """
    code_str = str(code)
    return len(code_str) == sequence_length and max(int(digit) for digit in code_str) <= color_count


def evaluate(guess: int, actual_code: int) -> Turn:
    """
    Evaluates a guess and returns an instance of class Turn.
    The Evaluation are split in two results: black and white pins.
    Black pins are the number of correctly guessed digits.
    White pins are the number of digits in the guess, which are contained in the actual code but are misplaced.

    Parameters
    ----------
    guess: int - the guessers guess 4 or 5 digits long. Can contain digits from 1 to 8
    actual_code: int - the code the guesser tries to guess

    Returns
    -------
    Turn - turn representation of the guess, as well as its evaluation aka. black pins and white pins
    """
    actual_code_as_str = str(actual_code)
    guess_as_str = str(guess)
    black_pins = 0
    white_pins = 0
    black_pin_set_at = []

    num_of_occurrences = {}
    for i in range(len(actual_code_as_str)):
        num_of_occurrences.setdefault(actual_code_as_str[i], 0)
        num_of_occurrences[actual_code_as_str[i]] += 1

    for i in range(len(actual_code_as_str)):
        if guess_as_str[i] == actual_code_as_str[i]:
            black_pins += 1
            num_of_occurrences[guess_as_str[i]] -= 1
            black_pin_set_at.append(i)

    for i in range(len(actual_code_as_str)):
        if i not in black_pin_set_at and num_of_occurrences.get(guess_as_str[i], 0) > 0:
            white_pins += 1
            num_of_occurrences[guess_as_str[i]] -= 1
    return Turn(guess, black_pins, white_pins)


def translate_to_pin_counts(feedback_string) -> tuple[int, int]:
    """
    Translates the feedback string into pin numbers.
    """
    black_pins = feedback_string.count("8")
    white_pins = feedback_string.count("7")
    return black_pins, white_pins