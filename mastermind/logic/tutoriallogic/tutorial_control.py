from mastermind.mvcinterfaces import Control
from .tutorial_ui import TutorialUI
from .tutorial_model import TutorialModel
from mastermind.navigation import NavigationManager


class TutorialControl(Control):
    id = -1  # -1 means not set yet

    def __init__(self, control_id):
        super().__init__(control_id)
        TutorialControl.id = control_id
        self.__ui = TutorialUI()
        self.__model = TutorialModel(self.__ui)

    @property
    def _ui(self) -> TutorialUI:
        return self.__ui

    @property
    def _model(self) -> TutorialModel:
        return self.__model

    def on_create(self, params):
        self._model.message = "Mit 'q' oder 'exit' beenden"
        self.__model.role = params

    def on_resume(self, params=""):
        self._start_ui()

    def on_pause(self):
        self._stop_ui()

    def on_destroy(self):
        pass

    def on_input_event(self, input_string):
        if input_string in ["exit", "q", "quit"]:
            NavigationManager.get_instance().finish()
