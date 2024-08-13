import unittest

from mastermind.logic.leaderboardlogic import LeaderboardModel
from mastermind.logic.leaderboardlogic.leaderboard_entry import LeaderboardEntry


class TestLeaderboardModel(unittest.TestCase):
    def setUp(self):
        self.leaderboard_model = LeaderboardModel()

    def test_empty_leaderboard(self):
        new_entry = LeaderboardEntry("Player1", 5, 120, 10, 3)
        position = self.leaderboard_model.compare_with_leaderboard(new_entry)
        self.assertEqual(position, 1)

    def test_add_to_empty_leaderboard(self):
        new_entry = LeaderboardEntry("Player1", 5, 120, 10, 3)
        self.leaderboard_model.insert_into_leaderboard(new_entry)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[0].number_of_turns, 5)

    def test_add_multiple_entries(self):
        entry1 = LeaderboardEntry("Player1", 5, 120, 10, 3)
        entry2 = LeaderboardEntry("Player2", 4, 150, 10, 3)
        entry3 = LeaderboardEntry("Player3", 6, 100, 10, 3)

        self.leaderboard_model.insert_into_leaderboard(entry1)
        self.leaderboard_model.insert_into_leaderboard(entry2)
        self.leaderboard_model.insert_into_leaderboard(entry3)

        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[0].number_of_turns, 4)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[1].number_of_turns, 5)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[2].number_of_turns, 6)

    def test_full_leaderboard(self):
        entries = [
            LeaderboardEntry("Player1", 1, 100, 10, 3),
            LeaderboardEntry("Player2", 2, 100, 10, 3),
            LeaderboardEntry("Player3", 3, 100, 10, 3),
            LeaderboardEntry("Player4", 4, 100, 10, 3),
            LeaderboardEntry("Player5", 5, 100, 10, 3),
            LeaderboardEntry("Player6", 6, 100, 10, 3),
            LeaderboardEntry("Player7", 7, 100, 10, 3),
            LeaderboardEntry("Player8", 8, 100, 10, 3),
            LeaderboardEntry("Player9", 9, 100, 10, 3),
            LeaderboardEntry("Player10", 10, 100, 10, 3)
        ]

        for entry in entries:
            self.leaderboard_model.insert_into_leaderboard(entry)

        new_entry = LeaderboardEntry("Player11", 5, 90, 10, 3)
        position = self.leaderboard_model.compare_with_leaderboard(new_entry)
        self.assertEqual(position, 5)

        self.leaderboard_model.insert_into_leaderboard(new_entry)

        self.assertEqual(len(self.leaderboard_model._LeaderboardModel__leaderboard), 10)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[4].number_of_turns, 5)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[4].playtime, 90)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[5].number_of_turns, 5)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[5].playtime, 100)
        self.assertEqual(self.leaderboard_model._LeaderboardModel__leaderboard[-1].number_of_turns, 9)

    def test_no_position_when_full_and_not_better(self):
        entries = [
            LeaderboardEntry("Player1", 1, 100, 10, 3),
            LeaderboardEntry("Player2", 2, 100, 10, 3),
            LeaderboardEntry("Player3", 3, 100, 10, 3),
            LeaderboardEntry("Player4", 4, 100, 10, 3),
            LeaderboardEntry("Player5", 5, 100, 10, 3),
            LeaderboardEntry("Player6", 6, 100, 10, 3),
            LeaderboardEntry("Player7", 7, 100, 10, 3),
            LeaderboardEntry("Player8", 8, 100, 10, 3),
            LeaderboardEntry("Player9", 9, 100, 10, 3),
            LeaderboardEntry("Player10", 10, 100, 10, 3)
        ]

        for entry in entries:
            self.leaderboard_model.insert_into_leaderboard(entry)

        new_entry = LeaderboardEntry("Player11", 10, 120, 10, 3)
        position = self.leaderboard_model.compare_with_leaderboard(new_entry)
        self.assertEqual(position, 0)


if __name__ == '__main__':
    unittest.main()
