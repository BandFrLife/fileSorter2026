"""
testing function, that checks listboxes are being filled correctly
"""
import unittest
import tkinter as tk
# from hypothesis import given
# import hypothesis.strategies as some

from gui2 import GUI
from guievents2 import Eventhandler


class TestEventhandler(unittest.TestCase):
    """class for testing the Movie class
    """
    def setUp(self) -> None:
        """setup movie for all testing
        """
        self.myevent = Eventhandler()
        self.varlistbox = tk.Listbox
        self.stalistbox = tk.Listbox

    def test_populatelist(self) -> None:
        """tests populatelist event
        """
        self.stalistbox.insert(tk.END, "test1.txt")
        self.stalistbox.insert(tk.END, "test2.txt")
        self.stalistbox.insert(tk.END, "test3.txt")
        self.myevent.populatelist(self.varlistbox)
        self.assertEqual(self.varlistbox, self.stalistbox)

    def test_setname(self) -> None:
        """tests setname function
        """

    def test_calccost(self) -> None:
        """tests calc_cost function
        """


class TestGui(unittest.TestCase):
    """class for testing the Processor class
    """
    def setUp(self) -> None:
        """setup procesor for all testing
        """
        self.myGui = GUI()

    def test_setcostlim(self) -> None:
        """tests set_costlim function
        """

    def test_checkcost(self) -> None:
        """test checkcost function
        """