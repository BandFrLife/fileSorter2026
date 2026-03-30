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
        self.tagoptions = ["Math", "English", "Science", "ComputerScience"]

    def makewindow(self):
        window = tk.Tk()
        window.title("File Sorter v0.2")
        window.geometry('900x500+75+75')  # window size(x,y), offest
        for row in range(5):
            window.rowconfigure(row, weight=1)
        for col in range(5):
            window.columnconfigure(col, weight=1)
        window.rowconfigure(0, weight=0)
        window.rowconfigure(2, weight=0)

        listscroll = tk.Scrollbar()
        filelist = tk.Listbox(window,
                              selectmode='multiple',
                              yscrollcommand=listscroll.set,
                              width=100,
                              height=100)

        dirpick = tk.Button(window,
                            text="Pick Directory",
                            anchor="ne",
                            padx=15,  # size of button in x
                            pady=3  # size of button in y
                            )
        dirpick.bind('<Button-1>', lambda event: Eventhandler.populatelist
                     ((), filelist))

        tagdropdown = tkk.Combobox(window,
                                   values=self.tagoptions,
                                   state="readonly",
                                   width=20
                                   )
        tagdropdown.set("Select a Subject")

        submit = tk.Button(window,
                           text="Save file",
                           anchor="se",
                           padx=20,  # size of button in x
                           pady=3  # size of button in y
                           )
        spacer = tk.Label(window,
                          text="Welcome to the File Sorter! "
                          "To start with pick your messy directory")

        listscroll = tk.Scrollbar(filelist,
                                  orient="vertical",
                                  )
#       Building the window, order matters
        dirpick.grid(row=1, column=0, padx=3, pady=2, sticky="nw")
        spacer.grid(row=0, column=0, pady=3, sticky="w")
        filelist.grid(row=1, column=0, padx=3, pady=5, sticky="w")
        listscroll.pack(pady=10, anchor="e")
        tagdropdown.grid(row=2, column=0, padx=3, pady=5, sticky="w")
        submit.grid(row=5, column=5, padx=3, pady=5, sticky="se")
        window.mainloop()

    def makeerror(self, errmess: str):
        """make an error window

        Returns:
            _type_: _description_
        """
        errwindow = tk.Tk()
        errwindow.title("File Sorter v0.1")
        errwindow.geometry('300x100+75+75')  # window size(x,y), offest
        for row in range(3):
            errwindow.rowconfigure(row, weight=2)
        for col in range(3):
            errwindow.columnconfigure(col, weight=2)
        errwindow.rowconfigure(0, weight=1)

        errlabel = tk.Label(errwindow,
                            text=errmess
                            )
        errlabel.grid(row=1, column=1, padx=5, pady=5)
        errwindow.attributes('-topmost', True)

        return 0


def main():
    window = GUI()
    window.makewindow()


if __name__ == "__main__":
    main()
# add constraints to what can be input
# entry/ add error catching for invalid entries
# add scrollbar that works
