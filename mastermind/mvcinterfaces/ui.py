from abc import ABC, abstractmethod
from .observer import Observer
import os


def clear_screen():
    """
    This function is always called right before draw()
    """
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux (name is 'posix')
    else:
        os.system('clear')


class UI(Observer, ABC):
    """
    Interface UI. Every Control should have an instance of this UI interface!
    The UI can be started with enable() and stopped with disable()
    until disable() is called this ui is stuck in a loop where it first draws content on the screen,
    then handles user input.
    UI frame size: width 46, height 24
    """

    __enabled = False

    _message = ""

    header = """
    ==============================================
                  Super-Superhirn
    ==============================================
    """

    @property
    def footer(self):
        """
        Returns the footer of the UI with the input prompt.
        """

        def wrap_text(text, line_length):
            """
            Wraps the given text to lines with a maximum length of line_length,
            resetting the length after a line break (\n).
            """

            def wrap_single_line(single_line, line_length):
                wrapped_lines = []
                while len(single_line) > line_length:
                    # Find the last space before the line_length limit
                    break_point = single_line.rfind(' ', 0, line_length)
                    if break_point == -1:
                        break_point = line_length
                    # Add the line to the list and trim the text
                    wrapped_lines.append(single_line[:break_point])
                    single_line = single_line[break_point:].lstrip()
                wrapped_lines.append(single_line)  # Add the remaining text as the last line
                return wrapped_lines

            lines = text.split('\n')
            wrapped_text = []
            for line in lines:
                wrapped_text.extend(wrap_single_line(line, line_length))
            return '\n'.join(wrapped_text)

        message_text = ""
        if self._message:
            message_lines = wrap_text(self._message, 46).split('\n')
            if len(message_lines) < 2:
                message_lines.append('')
            message_text = '\n'.join(f"    {line}" for line in message_lines) + '\n'
        else:
            message_text = "\n    \n"

        return ("    ==============================================\n"
                + message_text
                + "    ==============================================\n"
                + "    Eingabe:")

    def enable(self, event_listener):
        """
        Starts a loop where of calling
        :param event_listener: listener is called every time the user inputs a new line
        """
        self.__enabled = True
        while self.__enabled:
            self.repaint()
            # check user input
            user_input = input("  > ")
            event_listener(user_input.lower())

    def disable(self):
        """
        disables the ui loop
        """
        self.__enabled = False

    def generate_empty_lines(self, num_lines):
        return '\n' * num_lines

    @abstractmethod
    def draw(self):
        pass

    def repaint(self):
        """
        Clears screen and calls `draw()`
        Is called automatically in the UI-Loop. Use with caution.
        Used in the GuesserBot-Loop (where no player-inputs are needed during the game)
        """
        clear_screen()
        self.draw()

