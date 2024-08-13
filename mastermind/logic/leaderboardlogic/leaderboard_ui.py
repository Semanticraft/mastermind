from mastermind.mvcinterfaces import UI


def format_playtime(playtime_milliseconds):
    """
    Formats the playtime in milliseconds to a string in the format "mm:ss".
    If playtime is larger than 59:59, it returns "zz:ZZ".
    """
    total_seconds = int(playtime_milliseconds / 1000)
    if total_seconds > 3599:  # More than 59:59
        return "zz:ZZ"
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


class LeaderBoardUI(UI):
    """
    LeaderBoardUI class represents the UI of the leaderboard.
    """
    options = "    Optionen:                                 exit"

    sub_header = """
                    Leaderboard

    Rang | Name           | Züge | Zeit  | S/F
    ----------------------------------------------
    """

    def __init__(self):
        self.players = []

    def generate_leaderboard_table(self):
        """
        Generates the table for the leaderboard, including sequence length and color count.
        Adjusts the spacing to align data with the header.
        Ensures that the table always displays 10 lines, filling with empty lines if there are less than 10 players.
        """
        lines = []
        for rank, player in enumerate(self.players[:10], start=1):
            formatted_playtime = format_playtime(player.playtime)
            sequence_and_color = f"{player.sequence_length}/{player.color_count}"
            line = f" {rank:<2} | {player.name:<14} |  {player.number_of_turns:<3} | {formatted_playtime:<5} | {sequence_and_color}"
            lines.append(line)

        # Ensure there are always 10 lines
        while len(lines) < 10:
            lines.append(f" {len(lines) + 1:<2} | {'-':<14} |  {'-':<3} | {'-':<5} | {'-/-'}")

        return "\n     ".join(lines) + "\n"

    def draw(self):
        """
        Draws the leaderboard in the console.
        """
        content = self.generate_leaderboard_table()
        # print(self.options + self.header + self.sub_header + content + '\n' + self.footer)
        print(self.options, end="")
        print(self.header, end="")
        print(self.sub_header, end=" ")
        print(content)
        print(self.footer)

    def on_model_changed(self, model):
        """
        Updates the leaderboard data.
        """
        self.players = model.leaderboard
        self._message = model.message
