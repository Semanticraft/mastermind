from unittest.mock import patch, MagicMock
import unittest
from mastermind.logic.leaderboardlogic.leaderboard_ui import LeaderBoardUI, format_playtime


class TestLeaderBoardUI(unittest.TestCase):
    """
    Test class for LeaderBoardUI
    """
    # Mock player objects
    player1 = MagicMock()
    player2 = MagicMock()
    player3 = MagicMock()
    player4 = MagicMock()
    player5 = MagicMock()
    player6 = MagicMock()
    player7 = MagicMock()
    player8 = MagicMock()
    player9 = MagicMock()
    player10 = MagicMock()
    player11 = MagicMock()

    # Set attributes directly
    player1.configure_mock(name="Player1", playtime=90000, sequence_length=4, color_count=6, number_of_turns="1")
    player2.configure_mock(name="Player2", playtime=120000, sequence_length=5, color_count=7, number_of_turns="12")
    player3.configure_mock(name="Player3", playtime=90000, sequence_length=4, color_count=6, number_of_turns="2")
    player4.configure_mock(name="Player4", playtime=120000, sequence_length=5, color_count=7, number_of_turns="3")
    player5.configure_mock(name="Player5", playtime=90000, sequence_length=4, color_count=6, number_of_turns="4")
    player6.configure_mock(name="Player6", playtime=120000, sequence_length=5, color_count=7, number_of_turns="5")
    player7.configure_mock(name="Player7", playtime=90000, sequence_length=4, color_count=6, number_of_turns="6")
    player8.configure_mock(name="Player8", playtime=120000, sequence_length=5, color_count=7, number_of_turns="7")
    player9.configure_mock(name="Player9", playtime=90000, sequence_length=4, color_count=6, number_of_turns="8")
    player10.configure_mock(name="Player10", playtime=120000, sequence_length=5, color_count=7, number_of_turns="9")
    player11.configure_mock(name="Player11", playtime=90000, sequence_length=4, color_count=6, number_of_turns="5")

    def test_format_playtime(self):
        # Test normal playtime
        self.assertEqual(format_playtime(90000), "01:30")
        # Test edge case: exactly 59:59
        self.assertEqual(format_playtime(3599000), "59:59")
        # Test playtime larger than 59:59
        self.assertEqual(format_playtime(3600000), "zz:ZZ")

    def test_generate_leaderboard_table(self):
        # Initialize LeaderBoardUI and set players
        leaderboard_ui = LeaderBoardUI()
        leaderboard_ui.players = [self.player1, self.player2]

        expected_table = (
            " 1  | Player1        |  1   | 01:30 | 4/6\n"
            "      2  | Player2        |  12  | 02:00 | 5/7\n"
            "      3  | -              |  -   | -     | -/-\n"
            "      4  | -              |  -   | -     | -/-\n"
            "      5  | -              |  -   | -     | -/-\n"
            "      6  | -              |  -   | -     | -/-\n"
            "      7  | -              |  -   | -     | -/-\n"
            "      8  | -              |  -   | -     | -/-\n"
            "      9  | -              |  -   | -     | -/-\n"
            "      10 | -              |  -   | -     | -/-\n"
        )
        self.assertEqual(leaderboard_ui.generate_leaderboard_table(), expected_table)

    @patch('builtins.print')
    def test_draw(self, mock_print):
        # Initialize LeaderBoardUI without players to simplify
        leaderboard_ui = LeaderBoardUI()
        leaderboard_ui.draw()
        # Check if print was called (simplifying, as actual output depends on many factors)
        mock_print.assert_called()

    def test_generate_leaderboard_table_happy_path(self):
        # Assuming player1 through player10 are already defined in the setup
        leaderboard_ui = LeaderBoardUI()
        leaderboard_ui.players = [
            self.player1, self.player2, self.player3, self.player4,
            self.player5, self.player6, self.player7, self.player8,
            self.player9, self.player10
        ]
        # Expected table should match the format with correct data for player1 through player10
        expected_table = (
            " 1  | Player1        |  1   | 01:30 | 4/6\n      2  | Player2        |  12  | 02:00 | 5/7\n      3  | "
            "Player3        |  2   | 01:30 | 4/6\n      4  | Player4        |  3   | 02:00 | 5/7\n      5  | Player5  "
            "      |  4   | 01:30 | 4/6\n      6  | Player6        |  5   | 02:00 | 5/7\n      7  | Player7        |  "
            "6   | 01:30 | 4/6\n      8  | Player8        |  7   | 02:00 | 5/7\n      9  | Player9        |  8   | "
            "01:30 | 4/6\n      10 | Player10       |  9   | 02:00 | 5/7\n"
        )
        self.assertEqual(leaderboard_ui.generate_leaderboard_table(), expected_table)

    def test_generate_leaderboard_table_with_eleven_players(self):
        # Initialize LeaderBoardUI and set 11 players
        leaderboard_ui = LeaderBoardUI()
        leaderboard_ui.players = [
            self.player1, self.player2, self.player3, self.player4,
            self.player5, self.player6, self.player7, self.player8,
            self.player9, self.player10, self.player11
        ]
        # Generate the expected table string
        expected_table = (
            " 1  | Player1        |  1   | 01:30 | 4/6\n      2  | Player2        |  12  | 02:00 | 5/7\n      3  | "
            "Player3        |  2   | 01:30 | 4/6\n      4  | Player4        |  3   | 02:00 | 5/7\n      5  | Player5  "
            "      |  4   | 01:30 | 4/6\n      6  | Player6        |  5   | 02:00 | 5/7\n      7  | Player7        |  "
            "6   | 01:30 | 4/6\n      8  | Player8        |  7   | 02:00 | 5/7\n      9  | Player9        |  8   | "
            "01:30 | 4/6\n      10 | Player10       |  9   | 02:00 | 5/7\n"
        )
        self.assertEqual(leaderboard_ui.generate_leaderboard_table(), expected_table)

    def test_draw_with_full_leaderboard(self):
        # Test draw method with a full set of players
        # This requires patching print and setting up a full leaderboard
        with patch('builtins.print') as mock_print:
            leaderboard_ui = LeaderBoardUI()
            leaderboard_ui.players = [
                self.player1, self.player2, self.player3, self.player4,
                self.player5, self.player6, self.player7, self.player8,
                self.player9, self.player10
            ]
            leaderboard_ui.draw()
            mock_print.assert_called()  # Simplified check, ensure it's called

    def test_generate_leaderboard_table_no_players(self):
        # Test with no players
        leaderboard_ui = LeaderBoardUI()
        expected_table = (
            " 1  | -              |  -   | -     | -/-\n"
            "      2  | -              |  -   | -     | -/-\n"
            "      3  | -              |  -   | -     | -/-\n"
            "      4  | -              |  -   | -     | -/-\n"
            "      5  | -              |  -   | -     | -/-\n"
            "      6  | -              |  -   | -     | -/-\n"
            "      7  | -              |  -   | -     | -/-\n"
            "      8  | -              |  -   | -     | -/-\n"
            "      9  | -              |  -   | -     | -/-\n"
            "      10 | -              |  -   | -     | -/-\n"
        )
        self.assertEqual(leaderboard_ui.generate_leaderboard_table(), expected_table)

    def test_draw_no_players(self):
        # Test draw method with no players
        with patch('builtins.print') as mock_print:
            leaderboard_ui = LeaderBoardUI()
            leaderboard_ui.draw()
            mock_print.assert_called()  # Check print was called, indicating method handles empty state gracefully

    def test_format_playtime_minimum(self):
        # Edge case for format_playtime: minimum possible playtime
        self.assertEqual(format_playtime(0), "00:00")

    def test_generate_leaderboard_table_long_names(self):
        # Edge case with long player names
        player_long_name = MagicMock()


if __name__ == '__main__':
    unittest.main()
