"""main program file
"""
import tkinter as tk
from tkinter import ttk as tkk
import typing
from typing import Optional
from guievents import Eventhandler


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
        window.title("File Sorter v0.1")
        window.geometry('700x200+75+75')  # window size(x,y), offest
        for row in range(6):
            window.rowconfigure(row, weight=2)
        for col in range(6):
            window.columnconfigure(col, weight=2)
        window.rowconfigure(0, weight=1)

        pathentry = tk.Entry(window,
                             textvariable=tk.StringVar
                             (value="input Directory here"),
                             width=50
                             )
        pathentry.grid(row=1, column=0, padx=5, pady=7, sticky="w")

        pathpick = tk.Button(window,
                             text="Pick Directory",
                             anchor="ne",
                             padx=15,  # size of button in x
                             pady=3  # size of button in y
                             )
        pathpick.bind('<Button-1>', lambda event: Eventhandler.pickpath
                      ((), pathentry))
        pathpick.grid(row=1, column=1, padx=5, pady=7, sticky="w")

        fileentry = tk.Entry(window,
                             textvariable=tk.StringVar
                             (value="input File here"),
                             width=50
                             )
        fileentry.grid(row=2, column=0, padx=5, pady=7, sticky="w")

        filepick = tk.Button(window,
                             text="Pick File",
                             anchor="se",
                             padx=20,  # size of button in x
                             pady=3  # size of button in y
                             )
        filepick.bind('<Button-1>', lambda event: Eventhandler.pickfile
                      ((), fileentry))
        filepick.grid(row=2, column=1, padx=5, pady=7, sticky="w")

        tagdropdown = tkk.Combobox(window,
                                   values=self.tagoptions,
                                   state="readonly",
                                   width=20
                                   )
        tagdropdown.set("Select a Subject")
        tagdropdown.grid(row=3, column=0, padx=5, pady=7, sticky="w")

        submit = tk.Button(window,
                           text="Save file",
                           anchor="se",
                           padx=20,  # size of button in x
                           pady=3  # size of button in y
                           )
        submit.bind('<Button-1>',
                    lambda event: Eventhandler.savefileas((),
                                                          fileentry,
                                                          pathentry,
                                                          tagdropdown))
        submit.grid(row=6, column=6, padx=5, pady=7, sticky="se")

        window.mainloop()


def main():
    window = GUI()
    window.makewindow()


if __name__ == "__main__":
    main()
# add constraints to what can be input into
#  entry/ add error catching for invalid entries
