"""Seperate file that holds all events and calls from the gui

Returns:
    None: Nada, Nothing
"""
from tkinter.filedialog import askopenfilename, askdirectory
import os
import datetime
import tkinter as tk


class Eventhandler ():
    """_summary_
    """

    def pickfile(self, entry: tk.Entry) -> None:
        """_summary_

        Args:
            entry (tk.Entry): _description_

        Returns:
            str: _description_
        """
        entry.delete(0, tk.END)
        entry.insert(0, askopenfilename())

    def populatelist(self, box: tk.Listbox) -> None:
        """populates a ListBox with all the files in dir

        Args:
            entry (tk.ListBox): a ListBox to  input the data to

        """
        mylist = os.listdir(askdirectory())
        box.delete(0, tk.END)
        for file in mylist:
            box.insert(tk.END, file)

    def savefileas(self, file: tk.Entry,
                   directory: tk.Entry,
                   tag: tk.Entry) -> None:
        """the final function

        Args:
            file (tk.Entry): the file to save
            directory (tk.Entry): where to save it
            tag (tk.Entry): maybe add the tags in teh same function? idk yet
        """

    def prepfilestruct(self):
        semesterlist: list = ["Fall", "J-term", "Spring", "Summer"]
        date = datetime.datetime.now()
        year = date.strftime("%Y")
        for semester in semesterlist:
            try:
                yearsem = year+"/"+semester
                os.mkdir(yearsem)
                print(f"Directory '{yearsem}' created successfully.")
            except FileExistsError:
                print(f"Directory '{yearsem}' already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{yearsem}'.")

    # from gui import GUI

    # def errorhandle(self):
    #     GUI.makeerror((), "Function not implemented")
