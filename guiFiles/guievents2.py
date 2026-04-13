"""Seperate file that holds all events and calls from the gui

Returns:
    None: Nada, Nothing
"""
from tkinter.filedialog import askdirectory, asksaveasfile
import os
import datetime
import tkinter as tk


class Eventhandler ():
    """_summary_
    """

    def populatelist(self, box: tk.Listbox) -> None:
        """populates a ListBox with all the files in dir

        Args:
            entry (tk.ListBox): a ListBox to  input the data to

        """
        mylist = os.listdir(askdirectory())
        box.delete(0, tk.END)
        for file in mylist:
            box.insert(tk.END, file)

    def savefileas(self, filelist: tk.Listbox,
                   directory: str) -> None:
        """the final function

        Args:
            file (tk.Entry): the file to save
            directory (str): where to save it
            tag (str): maybe add the tags in teh same function? idk yet
        """
        # Currently falsifies file saving, needs adjustment
        for i in filelist.curselection():
            file = (filelist.get(i))
            asksaveasfile(
                mode="w",
                confirmoverwrite=True,
                initialdir=directory,
                initialfile=file
            )

    def prepfilestruct(self):
        semesterlist: list = ["Fall", "J-term", "Spring", "Summer"]
        date = datetime.datetime.now()
        year = date.strftime("%Y")
        try:
            os.mkdir(year)
            print(f"Directory '{year}' created successfully.")
        except FileExistsError:
            print(f"Directory '{year}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{year}'.")
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
