import subprocess
import platform


class TerminalOpener:
    """
    This class starts the mastermind game in a new terminal window.
    """

    def __init__(self, width=56, height=27):
        """
        Initializes the TerminalOpener with the given width and height.
        """
        self.__width = width
        self.__height = height

    def open_terminal(self, command_to_run):
        """
        Opens a new terminal window and runs the given command in it.
        """
        current_os = platform.system()
        if current_os == 'Darwin':  # macOS
            adjusted_command = f"printf '\\\\e[8;{self.__height};{self.__width}t'; {command_to_run}"
            apple_script_command = f'''
            tell application "Terminal"
                do script "{adjusted_command}"
                activate
                delay 1 -- Wait for the window to open
            end tell
            '''
            subprocess.run(['osascript', '-e', apple_script_command])
        elif current_os == 'Linux':  # Linux
            terminal_command = [f'gnome-terminal', f'--geometry={self.__width}x{self.__height}', '--', 'bash', '-c',
                                command_to_run]
            subprocess.run(terminal_command)
        elif current_os == 'Windows':  # Windows
            command = f'start cmd /k "mode con: cols={self.__width} lines={self.__height} & {command_to_run}"'
            subprocess.run(command, shell=True)


# Open a terminal window and run the mastermind game
opener = TerminalOpener()
opener.open_terminal('python -m mastermind.mastermind_initializer')
