"""main program file
"""
import tkinter as tk
from tkinter import ttk as tkk
import typing
from typing import Optional
from guievents2 import Eventhandler
from directory_model import DirectoryModel as DM


class GUI ():
    """ Singletone GUI class
    """
    _instance: Optional["GUI"] = None

    def __new__(cls,
                *args: tuple[typing.Any, ...],
                **kwargs: dict[typing.Any, typing.Any]
    ) -> "GUI":
        """Creates a new instance of the class if not already created.
           Enforces Singleton pattern.

        Returns:
            Solution: class instance of GUI
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # REPLACE WITH DirectoryModel class instead of hardcoding
        self.semesters: List[Semester] = []
        self.tags: List[Tag] = []

        self.dir_model = DM()

        self.selected_year = ""
        self.selected_semester = ""
        self.selected_class = ""

        self.yeardropdownframe = None
        self.semdropdownframe = None
        self.classdropdownframe = None

    def makewindow(self):
        """
        """
        #top level window
        window = tk.Tk()
        window.title("File Sorter v0.2")
        window.geometry('900x500+30+30')  # window size(x,y), offest

        # get up-to-date information
        years = self.dir_model.get_dirs("CMU")
        current_year = self.dir_model.get_current_year()
        current_semester = self.dir_model.get_current_semester()

        # update class based on up-to-date information
        self.selected_year = current_year
        self.selected_semester = current_semester

        #Config for grid layout
        #mostly expands some are static
        for row in range(5):
            window.rowconfigure(row, weight=1)
        for col in range(5):
            window.columnconfigure(col, weight=1)
        window.rowconfigure(0, weight=0)
        window.rowconfigure(2, weight=0)

        #frames group related widgets
        #keeps label+dropdown pairs organized
        #listboxframe = tk.Frame(window)  # for scrollable listbox
        yeardropdownframe = tk.Frame(window)  # for paired Semdropdown and label
        semdropdownframe = tk.Frame(window)  # for paired Semdropdown and label
        classdropdownframe = tk.Frame(window)  # for paired Tagdropdown and label

        # list to show fir contents
        #filelist = tk.Listbox(listboxframe,
        #                      selectmode='multiple',
        #                      width=30,
        #                      height=10)

        # button to open dir picker
        # current behavior depends on Eventhandler.populatelist(...)
        #dirpick = tk.Button(listboxframe,
        #                    text="Pick Directory",
        #                    anchor="ne",
        #                    padx=15,  # size of button in x
        #                    pady=3  # size of button in y
        #                    )

        self.yeardropdown = tkk.Combobox(yeardropdownframe,
                                   values=years,
                                   state="readonly",
                                   width=20
                                   )
        self.yeardropdown.set("Select a Year")

        #on click, open dir chooser and pop filelist
        # using command=... is better than bind(...)
        #dirpick.bind('<Button-1>', lambda event: Eventhandler.populatelist((), filelist))

        #sem dropdown
        self.semdropdown = tkk.Combobox(semdropdownframe,
                                   values=self.semester,
                                   state="readonly",
                                   width=20
                                   )
        self.semdropdown.set("Select a Semester")

        # class dropdown
        self.classdropdown = tkk.Combobox(classdropdownframe,
                                   values=self.classoptions,
                                   state="readonly",
                                   width=20
                                   )
        self.classdropdown.set("Select a Class")

        #save button
        submit = tk.Button(window,
                           text="Save file",
                           anchor="se",
                           padx=20,  # size of button in x
                           pady=3  # size of button in y
                           )

        #uses selected sem to build dest path
        # this is hardcoded
        #submit.bind('<Button-1>', lambda event: Eventhandler.savefileas
        #            ((), filelist, ("2026/"+self.semdropdown.get())))

        #intro text on win
        spacer = tk.Label(window,
                          text="Welcome to the File Sorter! "
                          "To start with pick your messy directory")

        # dropdown labels
        yearlabel = tk.Label(yeardropdownframe,
                            text="Pick your year")

        semlabel = tk.Label(semdropdownframe,
                            text="Pick your semester")

        classlabel = tk.Label(classdropdownframe,
                            text="Pick your class")


        #vertical scrollbar linked to the listbox
        #scrollbar = tk.Scrollbar(listboxframe,
        #                         orient="vertical",
        #                         command=filelist.yview
        #                         )
        #filelist.config(yscrollcommand=scrollbar.set)

        # ---------------------------
        # Build the window layout
        # ---------------------------
        # grid(...) is used on widgets placed directly in "window"
        # pack(...) is used inside each smaller frame

        #top message
        spacer.grid(row=0, column=0, pady=3, sticky="w")

        #frame containing the button, listbox, scrollbar
        #listboxframe.grid(row=1, column=0, sticky="w")

        #inside listboxfram:
        # button at top, listbox left, scroll bar right
        #dirpick.pack(side="top")
        #filelist.pack(side="left", fill="y")
        #scrollbar.pack(side="right", fill="y")

        #year section below listbox
        yeardropdownframe.grid(row=1, column=0, padx=3, pady=5, sticky="w")
        self.yeardropdown.pack(side="bottom")
        yearlabel.pack(side="top")

        #sem section below listbox
        semdropdownframe.grid(row=2, column=0, padx=3, pady=5, sticky="w")
        self.semdropdown.pack(side="bottom")
        semlabel.pack(side="top")

        #class section below semester
        classdropdownframe.grid(row=3, column=0, padx=3, pady=5, sticky="w")
        self.classdropdown.pack(side="bottom")
        classlabel.pack(side="top")

        #lower right save button
        submit.grid(row=5, column=5, padx=3, pady=5, sticky="se")

        #start tk loop event
        window.mainloop()

    def load_years(self) -> list[str]:
        """Loads directories labeled by year.
           From CMU/.
        """
        return self.dir_model.get_dirs("CMU")

    def load_semesters(self, year: str) -> list[str]:
        """Loads directories labeled by semester.
           From CMU/{given_year}/.
        """
        return self.dir_model.get_dirs(f"CMU/{year}")

    def load_classes(self, year: str, semester: str) -> list[str]:
        """Loads any directories labeled by class.
           CMU/{given_year}/{given_semester}/.
        """
        return self.dir_model.get_dirs(f"CMU/{year}/{semester}")

    def update_semesters(self, event=None) -> None:
        pass

    def update_classes(self, event=None) -> None:
        pass


def main():
    Eventhandler.prepfilestruct(())
    window = GUI()
    window.makewindow()


if __name__ == "__main__":
    main()
# add constraints to what can be input
# entry/ add error catching for invalid entries
# add scrollbar that works
