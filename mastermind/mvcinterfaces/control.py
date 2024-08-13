from abc import ABC, abstractmethod

from .ui import UI


class Control(ABC):
    """
    Interface Control which all ControlClasses should implement

    Each Control-Object has a Lifecycle.
    - First the control is in the off-state
    - It is invoked when on_create is called. Here it should set all needed attributes.
    - The control is now in the ready-state
    - Whenever on_resume is called the control is now fully active and its ui should start displaying the needed content
    - The control is now in the active-state
    - on_pause should pause the controller and make the ui erase everything from the console.
    - the ui is in the ready state again - so it can be reactivated by calling on_resume
    - When on_destroy is called all needed data should be saved (if needed)
    - it is now in the off-state again. It can be started again with on_create or deleted forever
    """

    def __init__(self, control_id):
        """
        Sets the id to control_id. Used for NavigationManager
        :param control_id: new value for id
        """
        self._id = control_id
        pass

    @property
    def id(self):
        """
        getter for the id
        :return: id of this control
        """
        return self._id

    @property
    @abstractmethod
    def _ui(self) -> UI:
        """
        each control should have an ui-instance
        :return: the ui instance
        """
        pass

    @property
    @abstractmethod
    def _model(self):
        """
        each control should have a model which the ui can read from
        :return: the model of this control
        """
        pass

    @abstractmethod
    def on_create(self, params):
        """
        called by NavigationManager whenever the control is activated. It is now in the ready state.
        The settings and ui should be set in this method
        :param params: different params which were passed to this control in navigate_to() method
        """
        pass

    @abstractmethod
    def on_resume(self, params):
        """
        called whenever the control should activate and display content to the console (via its ui)
        """
        pass

    @abstractmethod
    def on_pause(self):
        """
        called when the control should stop displaying content to the console. It is in the reaedy-state again and
        can be reactivated via on_resume()
        """
        pass

    @abstractmethod
    def on_destroy(self):
        """
        called whenever the control is removed from the navigation-stack. It is possible that this control is never
        activated again, so in here it should save important settings or attributes to a file.
        """
        pass

    @abstractmethod
    def on_input_event(self, input_string):
        """
        This method should be passed to the ui in
            setup_event_listeners(on_input_event)
        While this control is running, this method is called every time the user inputs a new line
        :param input_string: passes the line which was entered by the user
        :return: true or false whether the input_string could be processed or not
        """
        pass

    def _start_ui(self):
        """
        This method should be called in on_resume()
        """
        self._ui.enable(self.on_input_event)

    def _stop_ui(self):
        """
        This method should be called in on_pause()
        """
        self._ui.disable()
