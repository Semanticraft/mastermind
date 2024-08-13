from mastermind.mvcinterfaces import Control, UI
from .leaderboard_model import LeaderboardModel
from .leaderboard_ui import LeaderBoardUI
from ...navigation import NavigationManager


class LeaderboardControl(Control):
    id = -1  # -1 means not set yet

    __input_event_state = ""  # Empty string means view Leaderboard state

    def __init__(self, control_id):
        super().__init__(control_id)
        LeaderboardControl.id = control_id
        self.__ui = LeaderBoardUI()
        self.__model = LeaderboardModel(self.__ui)

    @property
    def _ui(self) -> LeaderBoardUI:  # was set to UI - why?
        return self.__ui

    @property
    def _model(self):
        return self.__model

    def on_create(self, params):
        """
        als params werden die Spieleinstellungen, die Zeit und Anzahl an Guesses übergeben.
        Those values are temporarily saved somewhere
        """

        self._model.leaderboard_entry = params
        if params == "from_menu":
            self._model.message = "S/F: Anzahl Codestellen/Farben \nMit 'exit' beenden"

        elif params != "":
            position = self.__model.compare_with_leaderboard(self._model.leaderboard_entry)
            if position > 0:
                self.__input_event_state = "confirm_save_score"
                self._model.message = f"Du hast Platz {position} erreicht!\nWillst du dein Ergebnis speichern? (Y/N)"
            else:
                self.__input_event_state = "restart_prompt"
                self._model.message = "Leider kein Highscore.\nGleiches Spiel nochmal starten? (Y/N)"
        else:
            self.__input_event_state = "restart_prompt"
            self._model.message = "Gleiches Spiel nochmal starten? (Y/N)"

    def on_resume(self, params=""):
        """
        make model deserialize leaderboard.
        give model values of recent game.
        let model check if values are good enough.
            maybe ask for name and insert values into leaderboard_list
        make model serialize leaderboard.
        """
        #  self._model.deserialize()
        self._start_ui()

    def on_pause(self):
        self._stop_ui()

    def on_destroy(self):
        pass

    def on_input_event(self, input_string):

        if input_string in ["exit", "quit", "q"]:
            NavigationManager.get_instance().finish()

        if self.__input_event_state == "confirm_save_score":
            if input_string in ["y", "Y", "yes", "Yes", "J", "j", "ja", "Ja"]:
                if not self._model.leaderboard_entry.name:
                    self._model.message = "Bitte trage deinen Namen ein"
                    self.__input_event_state = "enter_username"
                # TODO: maybe unreachable? (@Jaden)
                else:
                    self.__input_event_state = ""
                    self._model.message = "Dein Eintrag wurde gespeichert!*"
                    self._model.insert_into_leaderboard(self._model.leaderboard_entry)
            elif input_string in ["n", "N", "no", "No", "nein", "Nein"]:
                self.__input_event_state = "restart_prompt"
                self._model.leaderboard_entry = None
                self._model.message = "Eintrag wurde nicht gespeichert.\n" + "Gleiches Spiel nochmal starten? (Y/N)"
            else:
                self._model.message = "Falsche Eingabe! Möchtest du dein Ergebnis speichern? (Y/N)"

        elif self.__input_event_state == "enter_username":
            if len(input_string) < self._model.minimum_name_length:
                self._model.message = \
                    f"Mindestlänge des Namens ist {self._model.minimum_name_length}! Trage deinen Namen ein"
            elif len(input_string) > self._model.maximum_name_length:
                self._model.message = \
                    f"Maximallänge des Namens ist {self._model.maximum_name_length}! Trage deinen Namen ein"
            else:
                self._model.leaderboard_entry.name = input_string
                self._model.message = "Eintrag wurde gespeichert!" + "Gleiches Spiel nochmal starten? (Y/N)"
                self.__input_event_state = "restart_prompt"
                self._model.insert_into_leaderboard(self._model.leaderboard_entry)

        elif self.__input_event_state == "restart_prompt":
            if input_string in ["y", "Y", "yes", "Yes", "J", "j", "ja", "Ja"]:
                NavigationManager.get_instance().finish("restart_w_same_params")
            elif input_string in ["n", "N", "no", "No", "nein", "Nein"]:
                NavigationManager.get_instance().to_first_control()
