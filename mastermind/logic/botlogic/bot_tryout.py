from mastermind.logic.botlogic.guesser_bot_least_worst_case import GuesserBotLeastWorstCase
from mastermind.logic.botlogic.guesser_bot_unschaerfe import GuesserBotUnschaerfe
from mastermind.logic.gamelogic.game_logic import evaluate


# stole that for fast testing
def __evaluate(guess: int, actual_code: int):
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
    turn = evaluate(guess, actual_code)
    return turn.black_pins, turn.white_pins


if __name__ == '__main__':

    # # Testing a single code
    #
    # bot = GuesserBotLeastWorstCase(5, 8)
    # solution = "88888"
    # guess = 0
    # while guess != solution:
    #     guess = bot.guess()
    #     print(guess)
    #     feedback = evaluate(int(guess), int(solution))
    #     #print(feedback)
    #     bot.obtain_feedback(*feedback)

    # Testing multiple codes
    solutions4 = [
        '7343', '2741', '4342', '1716', '4352', '1562', '7214', '6358', '1218', '4278', '1716', '5236', '6243', '1218',
        '1632', '6414', '6414', '8318', '1632', '3542', '6414', '1517', '8314', '4615', '8671', '4278', '4653', '6358',
        '2717', '2656', '8856', '6237', '7867', '6561', '1434', '1218', '1517', '3542', '8671', '6243', '8671', '7214',
        '6243', '6237', '1218', '4615', '6414', '2656', '6824', '8671', '6237', '1716', '6358', '1716', '5568', '1218',
        '1517', '4352', '8318', '5456', '4342', '8317', '4342', '1517', '7343', '8246', '1434', '3845', '8671', '6237',
        '2656', '7343', '7867', '7424', '7867', '5236', '7214', '8317', '8856', '4615', '3845', '1218', '4278', '6824',
        '1218', '4844', '3845', '5236', '7343', '8314', '1434', '6358', '6237', '4844', '8318', '7867', '6824', '1434',
        '1517', '6414', '1716', '6237', '1517', '5568', '7867', '2656', '8586', '5568', '1632', '8317', '6414', '1716',
        '4844', '6414', '1562', '6824', '8586', '2357', '1517', '6414', '2656', '2357', '4278', '3845', '4844', '6824',
        '7867', '1434', '6243', '8586', '8671', '2656', '6358', '8671', '4615', '6824', '3845', '1434', '4278', '6358',
        '8586', '8317', '5568', '6358', '8246', '6237', '1517', '4278', '8314', '8317', '8317', '4342', '6824', '4278',
        '3534', '5568', '7424', '8314', '7867', '4352', '6237', '8856', '8314', '6561', '6358', '8586', '6414', '5568',
        '4615', '8246', '7867', '6824', '6243', '2656', '7424', '2656', '6243', '8317', '5236', '4342', '1434', '4278',
        '7214', '4278', '4342', '6824', '8856', '3845', '6824', '6243', '1716', '1434', '5456', '4844', '1434', '8586',
        '4278', '8317', '6237', '4342', '1434', '4653', '6358', '6561', '2357', '3534', '1562', '6243', '6358', '6358',
        '8318', '1562', '4342', '5236', '1716', '8318', '3542', '8314', '6237', '7424', '1632', '4342', '3534', '5456',
        '1632', '4653', '8671', '5456', '5568', '4653', '5236', '4342', '4342', '6237', '1632', '1716', '1716', '3534',
        '8586', '7867', '4615', '8856', '8586', '1445', '7867', '3534', '1218', '4844', '5456', '4844', '4278', '6358',
        '2741', '7424', '7867', '3542', '4278', '1434', '6243', '7214', '1632', '8671', '5568', '7214', '6358', '1445',
        '4653', '7424', '1517', '6414', '6243', '1562', '4342', '4653', '1445', '6237', '2741', '2656', '4653', '2656',
        '8586', '5236', '8856', '6243', '7343', '8671', '1632', '6237', '1517', '4653', '8671', '5568', '7214', '2357',
        '1562', '4342', '5568', '1632', '1716', '4278']

    solutions5 = [
        '37482', '67218', '54716', '16281', '48157', '82746', '57284', '78523', '63471', '31845',
        '12867', '27864', '84712', '36514', '75183', '86142', '28471', '17532', '64851', '32784',
        '15268', '81426', '37285', '26817', '57218', '68147', '54728', '71682', '45817', '38142',
        '71286', '57831', '46872', '12746', '84561', '28347', '16278', '78431', '52718', '31864']

    solution = solutions5
    overall_counter = 0
    fail_counter = 0
    for i in solution:
        # bot = GuesserBotLeastWorstCase(5, 8)
        bot = GuesserBotUnschaerfe(5, 8, 0.5)
        # bot.reset_lists(5, 8)
        guess = 0
        try:
            counter = 0
            while guess != i:
                guess = bot.guess()
                counter += 1
                print(guess)
                feedback = __evaluate(int(guess), int(i))
                #print(feedback)
                bot.obtain_feedback(*feedback)
            print("won")
            overall_counter += counter
        except Exception as e:
            print(e.args)
            print("fail")
            fail_counter += 1

    print("Avg-Guesses: ", overall_counter / (len(solution) - fail_counter))
    print("Fail-Quote: ", fail_counter / 100)
