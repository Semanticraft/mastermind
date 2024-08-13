from mastermind.mvcinterfaces import Control
from typing import Dict, List


class NavigationManager:
    """
    Class to navigate between different control-classes and manage their activity-states
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Returns _instance
        -------
        Singleton Instance of NavigationManager 
            if create_instance was used before.
        None 
            otherwise
        """
        return cls._instance

    @classmethod
    def create_instance(cls, control_map: Dict[int, Control]):
        """
        Creates an instance of the NavigationManager if there was none.
        Effectively makes the instance a singleton. 
        """
        if cls._instance is None:
            cls._instance = NavigationManager(control_map)

    def __init__(self, control_map: Dict[int, Control]):
        """
        Initiates the NavigationManager and its necessary attributes stack & map of controls
        """
        self.__control_map: Dict[int, Control] = control_map
        self.__control_stack: List[Control] = []  # initiate Stack for Control-Instances

    @property
    def __current_control(self):
        """
        Returns the currently active control if there is one.

        Returns
        -------
        self.__control_stack[-1], if the stack contains a control
        None otherwise
        """

        if len(self.__control_stack) > 0:
            return self.__control_stack[-1]
        return None

    def launch_control(self, control_id, params):
        """
        Pauses the current running control by calling on_pause(), and starts the control specified by control_id.
        the new control is pushed on the stack and started via on_create() and on_resume()

        Parameters
        ----------
        params: params passed to new control by calling on_create(params)
        control_id: control to be started

        Examples
        --------
        >>> from mastermind.navigation import NavigationManager
        >>> NavigationManager.get_instance().launch_control(GameControl.id)
        >>> # This control is about to pause
        """

        # initializing new control
        new_control = self.__control_map[control_id]  # TODO: what if control_id is not in map?  
        new_control.on_create(params)

        # Pausing current control
        if self.__current_control:
            self.__current_control.on_pause()

        # Starting new control
        self.__control_stack.append(new_control)
        self.__current_control.on_resume()

    def finish(self, params=""):
        """
        Stops running control by calling on_pause() followed by on_destroy() and removes it from the __control_stack.
        If the stack is not empty it takes the next control from its front and starts it by calling on_resume().
        If the stack is already empty the program is terminated.

        Examples
        --------
        >>> from mastermind.navigation import NavigationManager
        >>> NavigationManager.get_instance().finish()
        >>> # This control is about to shut down
        """

        # removing current control and resuming the one below with params
        if self.__current_control:
            old_control = self.__control_stack.pop()
            old_control.on_pause()
            old_control.on_destroy()

            if self.__current_control:
                self.__current_control.on_resume(params)

    def to_first_control(self):
        """
        Removes all controls from the stack except the first one (main_menu_control) and resumes it.
        """
        while len(self.__control_stack) > 1:
            old_control = self.__control_stack.pop()
            old_control.on_pause()
            old_control.on_destroy()
        self.__current_control.on_resume()

    def finish_and_launch(self, control_id, params):
        # TODO 14.06.2024 - implement
        pass
