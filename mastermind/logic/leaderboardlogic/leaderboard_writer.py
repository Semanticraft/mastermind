import json
from pathlib import Path
from typing import List
from mastermind.logic.leaderboardlogic import LeaderboardEntry


class LeaderboardWriter:
    """
    LeaderboardWriter class is responsible for writing the leaderboard data to a file.
    """
    @staticmethod
    def get_leaderboard_file_path() -> Path:
        current_script_dir = Path(__file__).resolve().parent
        leaderboard_file_path = (current_script_dir / '../../gamedata/leaderboard_data.json').resolve()
        return leaderboard_file_path

    @staticmethod
    def serialize(leaderboard: List[LeaderboardEntry]):
        with open(LeaderboardWriter.get_leaderboard_file_path(), 'w') as file:
            json.dump([entry.to_dict() for entry in leaderboard], file, indent=4)
