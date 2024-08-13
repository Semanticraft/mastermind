import time
import requests

from .game_logic import validate, evaluate, translate_to_pin_counts
from .game_ui import GameUI
from .game_model import GameModel
from mastermind.mvcinterfaces import Control
from mastermind.navigation import NavigationManager
from mastermind.logic.tutoriallogic import TutorialControl

from mastermind.logic.leaderboardlogic import LeaderboardControl, LeaderboardEntry

from .turn import Turn
from ..botlogic.guesser_bot_least_worst_case import GuesserBotLeastWorstCase
from ..botlogic.guesser_bot_unschaerfe import GuesserBotUnschaerfe
from ..botlogic.setter_bot_random import RandomSetterBot


def log_to_file(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")


class GameControl(Control):
    """
    GameControl class represents the Control of the game
    """
    id = -1  # -1 means not set yet

    def __init__(self, control_id):
        super().__init__(control_id)
        GameControl.id = control_id
        self.__ui = GameUI()
        self.__model = GameModel(self.__ui)

        self.__setter_bot = RandomSetterBot()
        self.__guesser_bot = GuesserBotUnschaerfe(5, 8, 0.5)
        self.__fast_guesser_bot = GuesserBotLeastWorstCase(5, 8)

    @property
    def _ui(self) -> GameUI:
        return self.__ui

    @property
    def _model(self):
        return self.__model

    def on_create(self, params):
        self._model.setup(*params)  # parameters are validated in main_menu_control

        if self._model.player_role == "guesser":
            self._model.code = self.__setter_bot.set_code(self._model.sequence_length, self._model.color_count)
            self._model.message = (f"Spiel erstellt mit CodeLänge {self._model.sequence_length} und "
                                   f"{self._model.color_count} Farben")
        else:
            self._model.message = "Bitte Code eingeben, der geraten werden soll."

    def on_resume(self, params=""):
        if params == "restart_w_same_params":
            # restart game with same params
            self._model.reset()
        self._start_ui()

    def on_pause(self):
        self._stop_ui()

    def on_destroy(self):
        pass

    def on_input_event(self, input_string: str):
        self._model.message = "Knapp daneben. Versuch's nochmal."
        if input_string == "exit" or input_string == "quit" or input_string == "q":
            NavigationManager.get_instance().finish()
        if input_string == "tutorial" or input_string == "t":
            NavigationManager.get_instance().launch_control(TutorialControl.id, self._model.player_role)

        if self._model.is_running:
            if self._model.player_role == "picker":
                self.picker_game(input_string)
            elif self._model.servercode_local_guesserbot:
                log_to_file("Servercode wird vom lokalen GuesserBot gelöst")
                self.bot_guesser_game(input_string)
            else:
                self.player_guesser_game(input_string)

        # maybe only as a temporary solution
        elif self._model.is_finished:
            # TODO for Daniil: Change to new Control Method
            new_entry = LeaderboardEntry("", self._model.guess_count, self._model.get_time_needed,
                                         self._model.sequence_length, self._model.color_count)
            # only give entry to leaderboard_control if the player was the guesser:
            payload = new_entry if self._model.player_role == "guesser" else ""
            NavigationManager.get_instance().launch_control(LeaderboardControl.id, payload)

    def picker_game(self, input_string: str):
        """
        Local Game Mode.
        Game loop of the bot guessing the right sequence.
        In this state picker_game is used once and will terminate after the bot successfully guessed the right sequence
        or exceeded the maximum amount of turns.
        """
        # resetting the bot to the right sequence length and color count
        self.__guesser_bot.reset_lists(self._model.sequence_length, self._model.color_count)

        try:
            code = int(input_string)
            if not validate(code, self._model.sequence_length, self._model.color_count):
                raise ValueError()
            self._model.code = code
            self._model.message = "Der Computer versucht nun den Code zu erraten."

        except ValueError:
            self._model.message = (f"Illegal Input! Input Guess of length {self._model.sequence_length} and "
                                   f"digits 1-{self._model.color_count}")
            return

        # loop of bot guessing:
        guess_counter = 0
        guess = 0
        while guess_counter < 12 and guess != self._model.code:

            starting_time = time.time_ns()
            guess = int(self.__guesser_bot.guess())                                       # bot is guessing
            feedback = evaluate(guess, self._model.code)                                  # evaluating the guess
            self.__guesser_bot.obtain_feedback(feedback.black_pins, feedback.white_pins)  # giving feedback to bot
            guess_counter += 1

            guessing_time = time.time_ns() - starting_time
            if guessing_time < 1_000_000_000:  # 1 second in nanoseconds
                time.sleep(
                    1. - guessing_time / 1_000_000_000)                                   # waiting for 1 second

            self._model.add_turn(evaluate(guess, self._model.code))                       # adding turn to model
            self.__ui.repaint()                                                           # re-drawing the ui

        self.end_of_game_check(guess=guess)

    def bot_guesser_game(self, input_string):
        """
        Online game mode.
        Mode in which the local bot is trying to guess the code set by a distant server.
        The latter also does the evaluation of the code.
        """
        # resetting the bot to the right sequence length and color count
        self.__fast_guesser_bot.reset_lists(self._model.sequence_length, self._model.color_count)

        # loop of bot guessing:
        guess_counter = 0
        guess = 0
        while guess_counter < 12:

            log_to_file(str(guess_counter))

            starting_time = time.time_ns()
            guess = int(self.__fast_guesser_bot.guess())

            # letting the server evaluate the guess
            response = self.feedback_from_server(guess, guess_counter == 0)
            if response is not None:

                guessing_time = time.time_ns() - starting_time
                if guessing_time < 1_000_000_000:  # 1 second in nanoseconds
                    time.sleep(
                        1. - guessing_time / 1_000_000_000)  # waiting for 1 second

                guess_counter += 1
                self.__fast_guesser_bot.obtain_feedback(*response)  # giving feedback to bot
                self._model.add_turn(Turn(guess, *response))
                self.__ui.repaint()  # re-drawing the ui
                if self._model.guess_history[-1].black_pins == self._model.sequence_length:
                    break
            else:
                self._model.message = "Server ist nicht mehr erreichbar. Mit 'exit' beenden."
                break

        if guess_counter > 0:
            self.end_of_game_check(guess=guess)

    def player_guesser_game(self, input_string: str):
        """
        Online or local game mode.
        """
        try:
            guess = int(input_string)
            if not validate(guess, self._model.sequence_length, self._model.color_count):
                raise ValueError()
        except ValueError:
            self._model.message = (f"Illegal Input! Input Guess of length {self._model.sequence_length} and "
                                   f"digits 1-{self._model.color_count}")
            return

        if self._model.game_mode == "lokal":
            self._model.add_turn(evaluate(guess, self._model.code))
        else:
            # letting the server evaluate the guess
            response = self.feedback_from_server(guess, self._model.guess_count == 0)
            if response is not None:
                self._model.add_turn(Turn(guess, *response))
            else:
                self._model.message = "Server ist nicht erreichbar. Erneut versuchen oder mit 'exit' beenden."

        self.end_of_game_check()

    def end_of_game_check(self, guess=-1):
        if ((self._model.guess_history[-1].black_pins == self._model.sequence_length)
                or (self._model.game_mode == "lokal" and guess == self._model.code)):
            self._model.finish_game(True)
            self._model.message = f" WON - Time: " + "{:.2f}".format(
                self._model.get_time_needed / 1000) + "s \n Weiter mit ENTER"  # temp

        elif self._model.board_filled:
            self._model.finish_game(False)
            self._model.message = f" LOST - Code was {self._model.code} \n Weiter mit ENTER"  # Temporary

    def feedback_from_server(self, guess, first_guess=False):
        """
        Sends a guess to the evaluation server and returns the response.
        """

        url = "http://" + self._model.ip_address + ":" + self._model.port + "/"

        initial_data = {
            "gameid": 0,
            "gamerid": self._model.gamer_id,
            "positions": self._model.sequence_length,
            "colors": self._model.color_count,
            "value": ""
        }

        if first_guess:
            # verbindungsaufbau:
            try:
                response = requests.post(url, json=initial_data)
                # setting game_id
                self._model.game_id = response.json()['gameid']

            except requests.exceptions.RequestException as e:
                print(f"HTTP Request failed: {e}")
                return None

        data = {
            "gameid": self._model.game_id,
            "gamerid": self._model.gamer_id,
            "positions": self._model.sequence_length,
            "colors": self._model.color_count,
            "value": guess
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                # retrieve feedback from response
                feedback_string = response.json()['value']
                # returning evaluation as tuple of black and white pins
                return translate_to_pin_counts(feedback_string)
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return None



