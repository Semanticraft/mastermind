class LeaderboardEntry:
    """
    LeaderboardEntry class represents a single entry in the leaderboard.
    """
    def __init__(self, player_name, number_of_turns, playtime, sequence_length, color_count):
        self.__name = player_name
        self.__number_of_turns = number_of_turns
        self.__time = playtime
        self.__sequence_length = sequence_length
        self.__color_count = color_count

    @property
    def number_of_turns(self):
        return self.__number_of_turns

    @property
    def playtime(self):
        return self.__time

    @property
    def name(self):
        return self.__name

    @property
    def sequence_length(self):
        return self.__sequence_length

    @property
    def color_count(self):
        return self.__color_count

    @name.setter
    def name(self, name):
        self.__name = name

    def to_dict(self):
        """
        Returns a dictionary representation of the LeaderboardEntry. Necessary for serialization.
        """
        return {
            "name": self.__name,
            "number_of_turns": self.__number_of_turns,
            "playtime": self.__time,
            "sequence_length": self.__sequence_length,
            "color_count": self.__color_count
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a LeaderboardEntry object from a dictionary representation of the LeaderboardEntry.
        """
        return cls(
            data["name"],
            data["number_of_turns"],
            data["playtime"],
            data["sequence_length"],
            data["color_count"]
        )
