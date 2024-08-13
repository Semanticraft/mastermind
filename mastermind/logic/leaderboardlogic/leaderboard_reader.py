import json
from pathlib import Path
from typing import List
from mastermind.logic.leaderboardlogic import LeaderboardEntry


class LeaderboardReader:
    """
    LeaderboardReader class is responsible for reading the leaderboard data from a file.
    """
    @staticmethod
    def get_leaderboard_file_path() -> Path:
        current_script_dir = Path(__file__).resolve().parent
        leaderboard_file_path = (current_script_dir / '../../gamedata/leaderboard_data.json').resolve()
        return leaderboard_file_path

    @staticmethod
    def deserialize() -> List[LeaderboardEntry]:
        try:
            with open(LeaderboardReader.get_leaderboard_file_path(), 'r') as file:
                data = json.load(file)
                return [LeaderboardEntry.from_dict(entry) for entry in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
