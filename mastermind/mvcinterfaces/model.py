from abc import ABC
from .observer import Observer


class Model(ABC):
    """
    Implements the observer pattern. has functionality to add, remove and notify observers.
    Since the UI interface extends Observer, UI can be updated as the model changes.
    """

    __message = ""

    def __init__(self, observer: Observer):
        """
        Initializes the model superclass.

        Parameters
        ----------
        observer: is saved in this class and can be updated via self._notify_observer()
        """
        self.__observer = observer
        observer.on_model_changed(self)  # TODO 14.06.2024 - Decide if updating right at start is smart or not

    @property
    def message(self):
        """
        This message is displayed in the footer of the UI

        Returns
        -------
        string - message to be displayed to the user
        """
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value
        self._notify_observer()

    def _notify_observer(self):
        """
        notifies every observer in the list of observers by calling Observer.on_model_changed(self)
        """
        self.__observer.on_model_changed(self)
