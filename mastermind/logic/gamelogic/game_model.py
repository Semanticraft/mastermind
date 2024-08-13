import random
from time import time
from typing import List

from .turn import Turn
from mastermind.mvcinterfaces import Model


def log_to_file(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")


class GameModel(Model):
    """
    GameModel class represents the Model of the game.
    """
    __player_as_guesser = True

    __lokal_game = True

    __ip_address = None

    __port = None

    __servercode_local_guesserbot = False

    __game_id = -1         # -1 means not set yet

    __gamer_id = -1        # -1 means not set yet

    __sequence_length = 5  # number between 4 and 5

    __color_count = 8      # number between 2 and 8

    __code = 00000

    __start_timestamp = 0

    __finish_timestamp = None

    __guess_history: List[Turn] = []

    __finished = False

    __won = False

    __error_message = ""

    def setup(self, sequence_length, color_count, player_as_guesser, lokal_game, ip_address, port, servercode_local_guesserbot):
        """
        Initializes the model for a new game! Sets needed game settings and calls reset()

        Parameters
        ----------
        sequence_length: int - length of the code to guess (4 or 5)
        color_count: int - number of different colors in the code (between 2 and 8)
        player_as_guesser: bool - True means player plays as guesser. False means player plays as picker
        lokal_game: bool - True means game is lokal. False means game is online
        ip_address: str - ip address of the server. Only used if game is online
        port: str - port of the server. Only used if game is online
        servercode_local_guesserbot: bool - True if the server code is solved by the local guesser bot
        """
        self.__sequence_length = sequence_length
        self.__color_count = color_count
        self.__player_as_guesser = player_as_guesser
        self.__lokal_game = lokal_game
        self.__ip_address = ip_address
        self.__port = port
        self.__servercode_local_guesserbot = servercode_local_guesserbot
        self.reset()  # reset calls _notify_observer()

    def reset(self):
        """
        Resets the Model, so it's ready for a new game.
        Resets timer, guess history, finished flag, etc.

        Can be called instead of setup:
        A new game will start but the Game Settings
        local_game, ip, port, sequence_length, color_count and player_as_guesser stay the same
        """
        self.__game_id = -1
        self.__gamer_id = random.Random().randint(1, 1000000) # randomly setting the gamer id
        self.__start_timestamp = time() * 1000
        self.__finish_timestamp = None
        self.__guess_history = []
        self.__finished = False
        self.__won = False
        self.message = f"Spiel erstellt mit CodeLänge {self.__sequence_length} und " \
                       f"{self.__color_count} Farben"
        self._notify_observer()

    def finish_game(self, won: bool):
        """
        Called whenever game ends. Stops timer

        Parameters
        ----------
        won: bool - whether the guesser guessed the code or not
        """
        self.__finish_timestamp = time() * 1000
        self.__finished = True
        self.__won = won
        self._notify_observer()

    @property
    def player_role(self) -> str:
        """
        Property player role. Can be picker or guesser

        Returns
        -------
        Role of the player - picker or guesser
        """
        if self.__player_as_guesser:
            return "guesser"
        else:
            return "picker"

    @property
    def game_mode(self) -> str:
        """
        Property game mode. Can be lokal or online

        Returns
        -------
        Game mode - lokal or online
        """
        if self.__lokal_game:
            return "lokal"
        else:
            return "online"

    @property
    def ip_address(self) -> str:
        """
        Property ip address. Only used if game mode is online

        Returns
        -------
        str - ip address
        """
        return self.__ip_address

    @property
    def port(self) -> str:
        """
        Property port. Only used if game mode is online

        Returns
        -------
        str - port
        """
        return self.__port

    @property
    def servercode_local_guesserbot(self) -> bool:
        """
        Property servercode local guesser bot. Only used if game mode is online

        Returns
        -------
        bool - servercode local guesser bot
        """
        return self.__servercode_local_guesserbot


    @property
    def game_id(self) -> int:
        """
        Property game id. Only used if game mode is online

        Returns
        -------
        int - game id
        """
        return self.__game_id

    @game_id.setter
    def game_id(self, value):
        """
        Setter for game id. sets the game id.

        Parameters
        ----------
        value: int - new value for the game id
        """
        self.__game_id = value

    @property
    def gamer_id(self) -> int:
        """
        Property gamer id. Only used if game mode is online

        Returns
        -------
        int - gamer id
        """
        return self.__gamer_id

    @property
    def sequence_length(self):
        """
        length of the code to guess. Can be 4 or 5

        Returns
        -------
        int - code length
        """
        return self.__sequence_length

    @property
    def color_count(self):
        """
        number of different colors. integer between 2 and 8

        Returns
        -------
        int - number of different colors
        """
        return self.__color_count

    @property
    def code(self):
        """
        Code Getter

        Returns
        -------
        int - the code which the guesser must guess
        """
        return self.__code

    @code.setter
    def code(self, value):
        """
        Setter for code. sets the code the guesser must guess and notifies the observer.
        Setting the code also starts the timer

        Parameters
        ----------
        value: int - new value for the code
        """
        self.__code = value
        self.__start_timestamp = time() * 1000
        self._notify_observer()

    @property
    def guess_history(self) -> List[Turn]:
        """
        Getter for guess history. list of instances Turn.
        has a maximum of 12 entries.

        Returns
        -------
        List[Turn] - entire guess history
        """
        return self.__guess_history

    def add_turn(self, turn: Turn):
        """
        adds turn to guess history and notifies observer

        Parameters
        ----------
        turn: turn to be added (of instance Turn)
        """
        self.__guess_history.append(turn)
        self._notify_observer()

    @property
    def guess_count(self):
        """
        returns the length of the guess history.
        This is the number of moves the player used.

        Returns
        -------
        int: len(self.__guess_history)
        """
        return len(self.__guess_history)

    @property
    def board_filled(self) -> bool:
        """
        Checks whether the board is filled or not.

        Returns
        -------
        bool: self.guess_count >= 12
        """
        return self.guess_count >= 12

    @property
    def get_time_needed(self):
        """
        Returns the time in ms the guesser needed to finish the game, after the code to guess has been set.

        Returns
        -------
        float: duration of game, if the game has finished, 0 else wise
        """
        if self.__finished:
            return self.__finish_timestamp - self.__start_timestamp
        else:
            return 0

    @property
    def start_timestamp(self):
        """
        Returns the time in ms when the game started.
        """
        return self.__start_timestamp

    @property
    def is_running(self):
        """
        returns true if game is currently running.
        Meaning the game has started (a code has been set) and is not over yet

        Returns
        -------
        bool - True if game is currently running.
        """
        return self.__start_timestamp and not self.__finished

    @property
    def is_finished(self):
        """

        """
        return self.__finished
