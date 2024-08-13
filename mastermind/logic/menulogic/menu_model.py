from mastermind.mvcinterfaces import Model


class MenuModel(Model):

    control_state = "initial"

    game_mode = ""

    ip_address = None

    port = None

    role = ""

    # in online mode, the bot should be able to guess
    servercode_local_guesserbot = False

    sequence_length = 0  # number between 4 and 5 (0 means not set)

    color_count = 0  # number between 2 and 8 (0 means not set)

    def all_set(self):
        """
        Returns
        -------
        bool - true if all the parameters to start a game have been set.
        """
        return self.role and self.sequence_length and self.color_count and self.game_mode and ((
                self.ip_address and self.port) if self.game_mode == "online" else True)

    def reset_all(self):
        """
        Resets all parameters back to their default values.
        """
        self.role = ""
        self.sequence_length = 0
        self.color_count = 0
        self.servercode_local_guesserbot = False
        self.game_mode = ""
        self.ip_address = None
        self.port = None
