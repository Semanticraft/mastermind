import ipaddress
import platform
import socket
import subprocess

from mastermind.mvcinterfaces.control import Control
from .menu_model import MenuModel
from .menu_ui import MenuUI
from ..gamelogic import GameControl
from ..leaderboardlogic.leaderboard_control import LeaderboardControl
from ..tutoriallogic import TutorialControl
from ...navigation import NavigationManager


def valid_id_address(ip_str):
    """
    Checks if the given string is a valid IP address and reachable.
    """
    try:
        # check if valid ip address
        ipaddress.ip_address(ip_str)
        # ping command of the operating system
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # running the ping command
        command = ['ping', param, '1', ip_str]
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # checking the result
        return response.returncode == 0

    except ValueError:
        return False


def valid_port(ip, port):
    """
    Checks if the given string is a reachable port on the given ip.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # setting timeout to 1 second
            result = s.connect_ex((ip, int(port)))  # trying to connect to the given ip and port
            if result == 0:
                return True  # port reachable
            else:
                return False  # port not reachable
    except Exception as e:
        # print(f"Ein Fehler ist aufgetreten: {e}")
        return False


class MainMenuControl(Control):
    """
    Control of the main menu. Responsible for handling the user input
    and starting the game control with the right parameters.
    """

    id = -1  # -1 means not set yet

    def __init__(self, control_id):
        super().__init__(control_id)
        MainMenuControl.id = control_id
        self.__ui = MenuUI()
        self.__model = MenuModel(self.__ui)

    @property
    def _model(self):
        return self.__model

    @property
    def _ui(self):
        return self.__ui

    def on_create(self, params):
        self._model.message = "Beispiele:     'lokal rater 4 7'\n   'online 127.0.0.1. 5000 rater_bot 5 2'"
        self._model.control_state = "initial"

    def on_resume(self, params=""):
        self._start_ui()

    def on_pause(self):
        self._stop_ui()

    def on_destroy(self):
        pass

    def game_params_validation(self, arguments):
        """
        Validates the game parameters and starts the game control with the right parameters.
        """
        if len(arguments) >= 1 and ((arguments[0] in ["rater", "setzer"])
                                    or (arguments[0] == "rater_bot" and self._model.game_mode == "online")):
            if arguments[0] == "rater_bot":
                self._model.role = "rater"
                self._model.servercode_local_guesserbot = True
            else:
                self._model.role = arguments[0]
                self._model.servercode_local_guesserbot = False
            arguments = arguments[1:]
            if len(arguments) >= 1 and arguments[0] in ["4", "5"]:
                self._model.sequence_length = int(arguments[0])
                arguments = arguments[1:]
                if len(arguments) >= 1 and arguments[0] in ["2", "3", "4", "5", "6", "7", "8"]:
                    self._model.color_count = int(arguments[0])
                    self._model.control_state = "initial"
                    game_control_params = self.get_model_paramlist()
                    NavigationManager.get_instance().launch_control(GameControl.id,
                                                                    game_control_params)
                else:
                    self._model.control_state = "request_color_count"
                    self._model.message = "Bitte als Anzahl der Farben eine Zahl zwischen 2 und 8 angeben."
            else:
                self._model.control_state = "request_sequence_length"
                self._model.message = "Bitte als Codelänge die Zahl 4 oder 5 angeben."
        else:
            self._model.control_state = "request_role"
            self._model.message = "Bitte als Rolle \"rater\" oder \"setzer\" angeben."

    def on_input_event(self, input_string):
        """
        Handling der Befehle:

            - starten (mit Argumenten)
                launch_control(GameControl.id, params) [params sind die values für länge/farben/rolle]

            - tutorial
                launch_control(TutorialControl.id, params)

            - q(uit)
                exit game

            - board
                launch_control(LeaderBoardControl.id, params)
        """
        # Commands which can always be executed
        if input_string == "q" or input_string == "quit":
            self._model.control_state = "initial"
            self._model.message = "Beispiel: 'lokal rater 4 7'"
            # NavigationManager.get_instance().finish()
        elif input_string == "tutorial" or input_string == "t":
            NavigationManager.get_instance().launch_control(TutorialControl.id, "")
        elif input_string in ["board", "leaderboard", "b"]:
            NavigationManager.get_instance().launch_control(LeaderboardControl.id, "from_menu")

        else:
            # Checking for state
            if self._model.control_state == "initial":
                arguments = []
                if input_string:
                    substrings = input_string.split()
                    arguments = substrings[1:]
                    input_string = substrings[0]
                # if input_string == "starten":
                if input_string in ["lokal", "online"]:
                    self._model.game_mode = input_string

                    if input_string == "online":
                        if len(arguments) >= 1 and valid_id_address(arguments[0]):
                            self._model.ip_address = arguments[0]
                            arguments = arguments[1:]

                            if len(arguments) >= 1 and valid_port(self._model.ip_address, arguments[0]):
                                self._model.port = arguments[0]
                                arguments = arguments[1:]
                                self.game_params_validation(arguments)

                            else:
                                self._model.control_state = "request_port"
                                self._model.message = "Bitte als Port eine gültige, erreichbare Portnummer angeben."
                        else:
                            self._model.control_state = "request_ip"
                            self._model.message = "Bitte als IP-Adresse eine gültige, erreichbare IP-Adresse angeben."
                    else:
                        self._model.ip_address = None
                        self._model.port = None
                        self.game_params_validation(arguments)

                else:
                    self._model.message = "Falscher Input - \"lokal\" oder \"online\" angeben."

            elif self._model.control_state == "request_ip":
                if valid_id_address(input_string):
                    self._model.ip_address = input_string
                    self._model.control_state = "request_port"
                    self._model.message = "Bitte als Port eine gültige, erreichbare Portnummer angeben."
                else:
                    self._model.message = "Falsche IP-Adresse - Bitte gültige, erreichbare IP-Adresse angeben."

            elif self._model.control_state == "request_port":
                if valid_port(self._model.ip_address, input_string):
                    self._model.port = input_string
                    self._model.control_state = "request_role"
                    self._model.message = "Bitte als Rolle \"rater\" oder \"setzer\" angeben."
                else:
                    self._model.message = "Falscher Port - Bitte gültige Portnummer angeben."

            elif self._model.control_state == "request_role":
                if (input_string in ["rater", "setzer"]) or (
                        input_string == "rater_bot" and self._model.game_mode == "online"):
                    if input_string == "rater_bot":
                        self._model.role = "rater"
                        self._model.servercode_local_guesserbot = True
                    else:
                        self._model.role = input_string
                    self._model.control_state = "request_sequence_length"
                    self._model.message = "Bitte als Codelänge die Zahl 4 oder 5 angeben."
                else:
                    self._model.message = "Falscher Input - \"rater\" oder \"setzer\" angeben."

            elif self._model.control_state == "request_sequence_length":
                input_string = input_string.strip()
                try:
                    input_int = int(input_string)
                    if input_int == 4 or input_int == 5:
                        self._model.sequence_length = input_int
                        self._model.control_state = "request_color_count"
                        self._model.message = "Bitte als Anzahl der Farben eine Zahl zwischen 2 und 8 angeben."
                    else:
                        self._model.message = "Codelänge muss 4 oder 5 sein"
                except ValueError:
                    self._model.message = "Codelänge muss eine Zahl sein!"

            elif self._model.control_state == "request_color_count":
                input_string = input_string.strip()
                try:
                    input_int = int(input_string)
                    if 2 <= input_int <= 8:
                        self._model.color_count = input_int
                        # TODO 18.06.2024 - Introduce new state if game can be started with same params
                        self._model.message = "Beispiel: 'lokal rater 4 7'"
                        self._model.control_state = "initial"
                        game_control_params = self.get_model_paramlist()
                        NavigationManager.get_instance().launch_control(GameControl.id, game_control_params)
                    else:
                        self._model.message = "Farb-Anzahl muss zwischen 2 und 8 sein"
                except ValueError:
                    self._model.message = "Farb-Anzahl muss zwischen 2 und 8 sein!!!"

    def get_model_paramlist(self):
        return [
            self._model.sequence_length, self._model.color_count,
            self._model.role == "rater", self._model.game_mode == "lokal",
            self._model.ip_address, self._model.port, self._model.servercode_local_guesserbot
        ]
