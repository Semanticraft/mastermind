import unittest
from unittest.mock import patch
from mastermind.logic.menulogic.main_menu_control import MainMenuControl


class TestMainMenuControl(unittest.TestCase):

    @patch('subprocess.run')
    def test_valid_ip_address_success(self, mock_subprocess):
        mock_subprocess.return_value.returncode = 0  # Simulate successful ping
        self.assertTrue(MainMenuControl.valid_ip_address("8.8.8.8"))

    @patch('subprocess.run')
    def test_valid_ip_address_failure(self, mock_subprocess):
        mock_subprocess.return_value.returncode = 1  # Simulate unsuccessful ping
        self.assertFalse(MainMenuControl.valid_ip_address("999.999.999.999"))

    @patch('socket.socket.connect_ex')
    def test_valid_port_success(self, mock_socket):
        mock_socket.return_value = 0  # Simulate successful connection
        self.assertTrue(MainMenuControl.valid_port("8.8.8.8", "53"))

    @patch('socket.socket.connect_ex')
    def test_valid_port_failure(self, mock_socket):
        mock_socket.return_value = 1  # Simulate unsuccessful connection
        self.assertFalse(MainMenuControl.valid_port("8.8.8.8", "99999"))


if __name__ == '__main__':
    unittest.main()
