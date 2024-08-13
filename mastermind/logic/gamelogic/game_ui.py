from mastermind.logic.gamelogic.game_model import GameModel
from mastermind.mvcinterfaces import UI, Observer
import datetime


def generate_hidden_code(sequence_length):
    """
    Generates the hidden code.
    """
    return f"                |   {'  '.join(['?'] * sequence_length)}   |"


def generate_section(game_rounds, sequence_length):
    """
    Generates the section of the game.
    """
    section = []
    empty_spaces = "  ".join([' '] * sequence_length)

    for i in range(12, 0, -1):
        if i <= len(game_rounds):
            first_number, second_number = list(reversed(game_rounds))[len(game_rounds) - i]
            formatted_first_number = "  ".join(str(first_number))
            line = f"  {i:>4} |   {formatted_first_number:<{sequence_length * 3 - 1}}  |  {second_number}"
        else:
            line = f"  {i:>4} |   {empty_spaces:<{sequence_length * 3 - 1}}  | "
        section.append("         " + line)

    return "\n".join(section)


def entries(guess_history, sequence_length):
    """
    Returns a list of tuples containing the guess and the corresponding evaluation.
    """
    eval_entries = []
    for turn in guess_history:
        eval_entries.append((turn.guess.__str__(), f"{'8' * turn.black_pins}{'7' * turn.white_pins}"
                             .ljust(sequence_length)))
    return eval_entries


def format_timestamp_to_24h_format(timestamp):
    """
    Formats the timestamp to a 24-hour time format string.
    """
    # Convert milliseconds to seconds
    total_seconds = timestamp / 1000
    # Create a datetime object from the timestamp
    dt_object = datetime.datetime.fromtimestamp(total_seconds)
    # Format the datetime object to a 24-hour time format string
    time_24h_format = dt_object.strftime('%H:%M')
    return time_24h_format


class GameUI(UI, Observer):
    """
    GameUI class represents the UI of the game.
    """
    __generated_section = "Section not generated yet"
    __generate_hidden_code = "Hidden code not generated yet"
    __options = "    Optionen:          (t)utorial             exit"
    __start_timestamp = ""

    def on_model_changed(self, model: GameModel):
        """
        Updates the game data.
        """
        sequence_length = model.sequence_length
        self.__generated_section = generate_section(entries(model.guess_history, sequence_length), sequence_length)
        self.__generate_hidden_code = generate_hidden_code(sequence_length)
        self._message = model.message
        self.__start_timestamp = model.start_timestamp

    def draw(self):
        """
        Draws the game in the console.
        """
        formatted_start_time = format_timestamp_to_24h_format(self.__start_timestamp)
        time = f"                                         {formatted_start_time}"
        print(self.__options, end="")
        print(self.header, end="")
        print(time)
        print()
        print(self.__generate_hidden_code)
        print(self.__generated_section)
        print()
        print(self.footer)
