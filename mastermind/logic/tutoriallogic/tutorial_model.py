from mastermind.mvcinterfaces import Model


class TutorialModel(Model):
    """
    TutorialModel class represents the model of the tutorial.
    """

    __role = "picker"

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        self.__role = value
        self._notify_observer()

