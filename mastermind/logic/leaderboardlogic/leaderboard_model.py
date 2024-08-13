from mastermind.logic.leaderboardlogic import LeaderboardEntry
from mastermind.mvcinterfaces import Model, Observer
from typing import List
from mastermind.logic.leaderboardlogic.leaderboard_reader import LeaderboardReader
from mastermind.logic.leaderboardlogic.leaderboard_writer import LeaderboardWriter


class LeaderboardModel(Model):
    """
    LeaderboardModel class represents the model of the leaderboard.
    """
    max_leaderboard_length = 10
    __leaderboard_entry: LeaderboardEntry
    minimum_name_length = 1
    maximum_name_length = 12
    __leaderboard: List[LeaderboardEntry] = []  # List of LeaderboardEntry instances

    def __init__(self, observer: Observer):
        super().__init__(observer)
        self.__leaderboard = LeaderboardReader.deserialize()

    def compare_with_leaderboard(self, entry: LeaderboardEntry):
        """
        Compares the given entry with the leaderboard and returns the position it should be inserted at.
        """
        position = 1  # Initialize position to 1 (top of the leaderboard)

        for current_entry in self.__leaderboard:
            if (entry.number_of_turns < current_entry.number_of_turns or
                    (entry.number_of_turns == current_entry.number_of_turns and
                     entry.playtime < current_entry.playtime)):
                return position
            position += 1

        if len(self.__leaderboard) < self.max_leaderboard_length:
            return position

        return 0

    def insert_into_leaderboard(self, entry: LeaderboardEntry):
        """
        Inserts the entry into the leaderboard if it is good enough.
        """
        position = self.compare_with_leaderboard(entry)
        if position > 0:
            self.__leaderboard.insert(position - 1, entry)
            if len(self.__leaderboard) > self.max_leaderboard_length:
                self.__leaderboard.pop(-1)
            self._notify_observer()
            LeaderboardWriter.serialize(self.__leaderboard)

    @property
    def leaderboard_entry(self) -> LeaderboardEntry:
        return self.__leaderboard_entry

    @leaderboard_entry.setter
    def leaderboard_entry(self, entry: LeaderboardEntry):
        self.__leaderboard_entry = entry
        self._notify_observer()

    @property
    def leaderboard(self) -> List[LeaderboardEntry]:
        return self.__leaderboard
