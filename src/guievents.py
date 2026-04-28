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
        deny = "Permission denied:"

        for i in range(4):
            try:
                os.mkdir(prefix + str(year + i))
                print(
                    f"'{prefix + str(year + i)}/' created successfully.")
            except FileExistsError:
                print(f"'{prefix + str(year + i)}/' already exists.")
            except PermissionError:
                print(f"{deny} Unable to create '{prefix + str(year + i)}/'.")

            for semester in semesterlist:
                try:
                    yearsem = prefix + str(year + i) + "/" + semester
                    os.mkdir(yearsem)
                    print(f"'{yearsem}/' created successfully.")
                except FileExistsError:
                    print(f"'{yearsem}/' already exists.")
                except PermissionError:
                    print(f"{deny} Unable to create '{yearsem}/'.")

    def get_current_year(self) -> int:
        return int(datetime.datetime.now().year)

    def get_current_semester(self) -> int:
        month = int(datetime.datetime.now().month)
        day = int(datetime.datetime.now().day)

        if month == 1 and day < 14:
            if day < 14:
                return 'J-term'
        elif month < 5:
            return 'Spring'
        elif month < 8:
            return 'Summer'
        else:
            return 'Fall'

    # from gui import GUI

    # def errorhandle(self):
    #     GUI.makeerror((), "Function not implemented")
