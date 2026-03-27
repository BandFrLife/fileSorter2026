"""Seperate file that holds all events and calls from the gui

Returns:
    None: Nada, Nothing
"""
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter as tk


class Eventhandler ():
    """_summary_
    """

    def pickfile(self, entry: tk.Entry) -> str:
        """_summary_

        Args:
            entry (tk.Entry): _description_

        Returns:
            str: _description_
        """
        entry.delete(0, tk.END)
        entry.insert(0, askopenfilename())

    def pickpath(self, entry: tk.Entry) -> str:
        """_summary_

        Args:
            entry (tk.Entry): _description_

        Returns:
            str: _description_
        """
        entry.delete(0, tk.END)
        entry.insert(0, askdirectory())

    def savefileas(self, file: tk.Entry,
                   directory: tk.Entry,
                   tag: tk.Entry) -> None:
        """the final function

        Args:
            file (tk.Entry): the file to save
            directory (tk.Entry): where to save it
            tag (tk.Entry): maybe add the tags in teh same function? idk yet
        """
