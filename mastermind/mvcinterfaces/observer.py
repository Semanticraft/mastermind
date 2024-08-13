from abc import ABC, abstractmethod


class Observer(ABC):
    """
    This interface follows the observer-pattern.
    The UI interface extends this interface, since UI should get update notifications whenever the model changes.
    """

    @abstractmethod
    def on_model_changed(self, model):
        """
        Should be called by the model every time it changes.
        Here the UI (which overrides this method) should update the text data it displays to the screen

        Parameters
        ----------
        model: the updated value of the model
        """
        pass
