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

    def savefileas(self, filelist: tk.Listbox, directory: str) -> None:
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
        year = int(date.strftime("%Y"))
        prefix = ("CMU/")
        print(prefix)

        for i in range(4):
            try:
                os.mkdir(prefix+str(year+i))
                print(f"Directory '{prefix+str(year+i)}' created successfully.")
            except FileExistsError:
                print(f"Directory '{prefix+str(year+i)}' already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{prefix+str(year+i)}'.")

            for semester in semesterlist:
                try:
                    yearsem = prefix+str(year+i)+"/"+semester
                    os.mkdir(yearsem)
                    print(f"Directory '{yearsem}' created successfully.")
                except FileExistsError:
                    print(f"Directory '{yearsem}' already exists.")
                except PermissionError:
                    print(f"Permission denied: Unable to create '{yearsem}'.")

    # from gui import GUI

    # def errorhandle(self):
    #     GUI.makeerror((), "Function not implemented")
