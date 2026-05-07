"""
Unittesting GUI class

ALL CHATGPT
Not too sure how to do a lot of this for a gui.
"""

import unittest
from unittest.mock import patch, MagicMock

from src.gui2 import GUI


class TestGUI(unittest.TestCase):
    """
    Unittesting GUI class
    """

    def setUp(self) -> None:
        """ Sets up GUI instance to do specific tests """
        GUI._instance = None
        self.g = GUI()

    def test_GUI_constructor(self) -> None:
        """ Test the constructor of GUI """
        self.assertEqual(
            self.g.default_tags,
            [
                "2026",
                "Fall",
                "Homework",
                "Notes",
                "Lab",
                "Project",
                "Exam",
            ],
        )
        self.assertEqual(
            self.g.semesters,
            ["Fall", "J-term", "Spring", "Summer"],
        )
        self.assertIsNotNone(self.g.events)

    def test_GUI_singleton(self) -> None:
        """Tests that GUI only creates one instance."""
        g2 = GUI()

        self.assertIs(self.g, g2)

    @patch("src.gui2.tk.Tk")
    def test_makewindow(self, mock_tk: MagicMock) -> None:
        """Tests makewindow without opening the real GUI."""
        mock_window = MagicMock()
        mock_tk.return_value = mock_window

        self.g.events = MagicMock()
        self.g.makewindow()

        self.g.events.prepfilestruct.assert_called_once()
        mock_window.title.assert_called_once_with("File Sorter v0.3")
        mock_window.geometry.assert_called_once_with("900x500")
        mock_window.mainloop.assert_called_once()

    @patch("src.gui2.GUI")
    def test_main(self, mock_gui: MagicMock) -> None:
        """Tests main creates GUI and calls makewindow."""
        mock_window = MagicMock()
        mock_gui.return_value = mock_window

        GUI.main()

        mock_gui.assert_called_once()
        mock_window.makewindow.assert_called_once()
