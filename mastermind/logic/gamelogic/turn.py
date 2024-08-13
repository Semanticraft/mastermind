class Turn:
    """
    entry for guess history.
    Contains the actual guess as string, as well as the evaluation as two ints (black and white pins)
    """

    def __init__(self, guess: int, black_pins: int, white_pins: int):
        """
        Constructor for Turn. Sets all attributes to the values passed as parameters.
        These cannot be changed but can be accessed (they are effectively final)

        Parameters
        ----------
        guess: int - the guess
        black_pins: int - number of colors at correct plays
        white_pins: int - number of colors which are contained but are at the wrong place
        """
        self.__guess = guess
        self.__black_pins = black_pins
        self.__white_pins = white_pins

    @property
    def guess(self):
        """
        Getter for guess

        Returns
        -------
        the guess of this turn
        """
        return self.__guess

    @property
    def black_pins(self):
        """
        Getter for black_pins

        Returns
        -------
        the black_pins count of this turn
        """
        return self.__black_pins

    @property
    def white_pins(self):
        """
        Getter for white_pins

        Returns
        -------
        the white_pins count of this turn
        """
        return self.__white_pins
