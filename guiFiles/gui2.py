"""main program file
"""
import tkinter as tk
from tkinter import ttk as tkk
import typing
from typing import Optional
from guievents2 import Eventhandler


class GUI ():
    _instance: Optional["GUI"] = None

    def __new__(cls, *args: tuple[typing.Any, ...],
                **kwargs: dict[typing.Any, typing.Any]
                ) -> "GUI":
        """Creates a new instance of the class if not already created.

        Enforces Singleton pattern.

        Returns:
            Solution: class instance
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.tagoptions = ["Math", "English", "Labs", "ComputerScience"]
        self.semester = ["None", "Fall", "J-term", "Spring", "Summer"]

    def makewindow(self):
        window = tk.Tk()
        window.title("File Sorter v0.2")
        window.geometry('900x500+30+30')  # window size(x,y), offest
        for row in range(5):
            window.rowconfigure(row, weight=1)
        for col in range(5):
            window.columnconfigure(col, weight=1)
        window.rowconfigure(0, weight=0)
        window.rowconfigure(2, weight=0)
        listboxframe = tk.Frame(window)  # for scrollable listbox
        tagdropdownframe = tk.Frame(window)  # for paired Tagdropdown and label
        semdropdownframe = tk.Frame(window)  # for paired Semdropdown and label

        filelist = tk.Listbox(listboxframe,
                              selectmode='multiple',
                              width=30,
                              height=10)

        dirpick = tk.Button(listboxframe,
                            text="Pick Directory",
                            anchor="ne",
                            padx=15,  # size of button in x
                            pady=3  # size of button in y
                            )
        dirpick.bind('<Button-1>', lambda event: Eventhandler.populatelist
                     ((), filelist))

        tagdropdown = tkk.Combobox(tagdropdownframe,
                                   values=self.tagoptions,
                                   state="readonly",
                                   width=20
                                   )
        tagdropdown.set("Select a Class")

        semdropdown = tkk.Combobox(semdropdownframe,
                                   values=self.semester,
                                   state="readonly",
                                   width=20
                                   )
        semdropdown.set("Select a Semester")

        submit = tk.Button(window,
                           text="Save file",
                           anchor="se",
                           padx=20,  # size of button in x
                           pady=3  # size of button in y
                           )
        submit.bind('<Button-1>', lambda event: Eventhandler.savefileas
                    ((), filelist, ("2026/"+semdropdown.get())))
        spacer = tk.Label(window,
                          text="Welcome to the File Sorter! "
                          "To start with pick your messy directory")

        taglabel = tk.Label(tagdropdownframe,
                            text="Pick your class")

        semlabel = tk.Label(semdropdownframe,
                            text="Pick your semester")

        scrollbar = tk.Scrollbar(listboxframe,
                                 orient="vertical",
                                 command=filelist.yview
                                 )
        filelist.config(yscrollcommand=scrollbar.set)

#       Building the window, order matters
        spacer.grid(row=0, column=0, pady=3, sticky="w")
        listboxframe.grid(row=1, column=0, sticky="w")
        dirpick.pack(side="top")
        filelist.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")
        tagdropdownframe.grid(row=2, column=0, padx=3, pady=5, sticky="w")
        tagdropdown.pack(side="bottom")
        taglabel.pack(side="top")
        semdropdownframe.grid(row=3, column=0, padx=3, pady=5, sticky="w")
        semdropdown.pack(side="bottom")
        semlabel.pack(side="top")
        submit.grid(row=5, column=5, padx=3, pady=5, sticky="se")
        window.mainloop()


def main():
    Eventhandler.prepfilestruct(())
    window = GUI()
    window.makewindow()


if __name__ == "__main__":
    main()
# add constraints to what can be input
# entry/ add error catching for invalid entries
# add scrollbar that works
