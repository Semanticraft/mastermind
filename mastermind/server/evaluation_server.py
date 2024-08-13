from flask import Flask, request, jsonify

from mastermind.logic.botlogic.setter_bot_random import RandomSetterBot
from mastermind.logic.gamelogic.game_logic import evaluate


class EvaluationServer:
    """
    This class acts as a server of evaluations for clients that connect with it.
    """
    __game_counter = 0
    __setter_bot = RandomSetterBot()
    __actual_code_dict = {}

    def __init__(self):
        """
        Initializes the Flask app and sets up the routes.
        """
        self.app = Flask(__name__)
        self.add_routes()

    def add_routes(self):
        """
        Adds routes to the Flask app.
        """
        self.app.add_url_rule('/', view_func=self.evaluate, methods=['POST'])

    def new_game(self, positions: int, colors: int) -> int:
        """
        Starts a new game with the given number of positions and colors.

        Args:
            positions (int): The number of positions in the code.
            colors (int): The number of different colors that can be used in the code.

        Returns:
            int: The unique game ID for the new game.
        """
        self.__game_counter += 1
        self.__actual_code_dict[self.__game_counter] = self.__setter_bot.set_code(positions, colors)
        return self.__game_counter

    def evaluate(self):
        """
        Evaluates a guess submitted by a client.
        If the game ID is 0, a new game is started.

        Request JSON structure:
        {
            "gameid": int,
            "gamerid": str,
            "positions": int,
            "colors": int,
            "value": str
        }

        Returns:
            Response (json): JSON object containing the evaluation result.
            If any required field is missing, a 400 error is returned.
        """
        data = request.json

        try:
            gameid = data['gameid']
            gamerid = data['gamerid']
            positions = data['positions']
            colors = data['colors']
            value = data['value']
        except KeyError as e:
            return jsonify({"error": f"Missing field {str(e)}"}), 400

        if gameid != 0:
            turn = evaluate(value, self.__actual_code_dict[gameid])
            value = "8" * turn.black_pins + "7" * turn.white_pins

        gameid = gameid if gameid != 0 else self.new_game(positions, colors)

        response_data = {
            "gameid": gameid,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": value
        }

        return jsonify(response_data), 200

    def run(self):
        """
        Runs the Flask app on any private and public IP address of the local machine and localhost on port 5000.
        """
        self.app.run(host='0.0.0.0', port=5000)


# maybe add a main menu point, or let this run in a background thread instead
if __name__ == '__main__':
    api = EvaluationServer()
    api.run()
