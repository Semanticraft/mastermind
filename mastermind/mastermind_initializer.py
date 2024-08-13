"""
This module is the starter-module for the whole project.
The NavigationManager is initialized and started from here.
Other important configurations also are set in this module.
"""

from typing import Dict

from mastermind.logic.gamelogic.game_control import GameControl
from mastermind.logic.leaderboardlogic.leaderboard_control import LeaderboardControl
from mastermind.logic.menulogic.main_menu_control import MainMenuControl
from mastermind.logic.tutoriallogic.tutorial_control import TutorialControl
from mastermind.mvcinterfaces import Control
from mastermind.navigation import NavigationManager
from mastermind.logic.leaderboardlogic.leaderboard_entry import LeaderboardEntry  # important even if gray
import os

os.environ['TERM'] = 'xterm-256color'  # set TERM environment variable to xterm-256color for color support in terminal

if __name__ == '__main__':
    control_map: Dict[int, Control] = {  # initialize control map
        0: MainMenuControl(0),
        1: GameControl(1),
        2: TutorialControl(2),
        3: LeaderboardControl(3)
    }
    NavigationManager.create_instance(control_map)  # create navigation manager instance
    NavigationManager.get_instance().launch_control(MainMenuControl.id, "Initial Parameter")  # launch program
