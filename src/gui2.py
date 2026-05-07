"""Main program file for the file sorter GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import typing
from typing import Optional
from guievents2 import Eventhandler
from guisort import sortGUI


class GUI:
    """Builds the file sorter window."""

    _instance: Optional["GUI"] = None

    def __new__(
        cls,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[typing.Any, typing.Any],
    ) -> "GUI":
        """Create one GUI instance only."""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.default_tags = [
            "2026",
            "Fall",
            "Homework",
            "Notes",
            "Lab",
            "Project",
            "Exam",
        ]
        self.semesters = ["Fall", "J-term", "Spring", "Summer"]
        self.events = Eventhandler()
        self.sortwindow = sortGUI

    def makemainwindow(self) -> None:
        """Create and run the main Tkinter window."""
        self.events.prepfilestruct()

        window = tk.Tk()
        window.title("File Sorter v0.3")
        window.geometry("900x500")

        for row in range(6):
            window.rowconfigure(row, weight=1)
        for col in range(4):
            window.columnconfigure(col, weight=1)

        file_frame = tk.Frame(window)
        semester_frame = tk.Frame(window)
        course_frame = tk.Frame(window)
        tag_frame = tk.Frame(window)

        welcome = tk.Label(
            window,
            text="Pick a directory, select files, "
                 "add class/semester/tags, then save.",
        )

        filelist = tk.Listbox(
            file_frame,
            selectmode="multiple",
            width=35,
            height=14,
            exportselection=False
        )

        scrollbar = tk.Scrollbar(
            file_frame,
            orient="vertical",
            command=filelist.yview,
        )
        filelist.config(yscrollcommand=scrollbar.set)

        dirpick = tk.Button(
            file_frame,
            text="Pick Directory",
            padx=15,
            pady=3,
            command=lambda: self.events.populatelist(filelist),
        )

        sem_label = tk.Label(semester_frame, text="Semester")
        sem_dropdown = ttk.Combobox(
            semester_frame,
            values=self.semesters,
            state="readonly",
            width=20,
        )
        sem_dropdown.set("Select a Semester")

        course_label = tk.Label(course_frame, text="Class / Course Name")
        course_entry = tk.Entry(course_frame, width=24)

        tag_label = tk.Label(tag_frame, text="Tags")
        tag_list = tk.Listbox(
            tag_frame,
            selectmode="multiple",
            width=24,
            height=8,
            exportselection=False
        )
        for tag in self.default_tags:
            tag_list.insert(tk.END, tag)

        tag_entry = tk.Entry(tag_frame, width=24)
        add_tag = tk.Button(
            tag_frame,
            text="Add Tag",
            command=lambda: self.events.add_tag(tag_entry, tag_list),
        )

        submit = tk.Button(
            window,
            text="Save file",
            padx=20,
            pady=3,
            command=lambda: self.events.savefileas(
                filelist,
                sem_dropdown.get(),
                course_entry.get(),
                tag_list,
            ),
        )

        # Window layout
        welcome.grid(row=0, column=0, columnspan=4, pady=8, sticky="w")

        file_frame.grid(
            row=1,
            column=0,
            rowspan=4,
            padx=8,
            pady=5,
            sticky="nw")
        dirpick.pack(side="top", anchor="w")
        filelist.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")

        semester_frame.grid(row=1, column=1, padx=8, pady=5, sticky="nw")
        sem_label.pack(side="top", anchor="w")
        sem_dropdown.pack(side="top", anchor="w")

        course_frame.grid(row=2, column=1, padx=8, pady=5, sticky="nw")
        course_label.pack(side="top", anchor="w")
        course_entry.pack(side="top", anchor="w")

        tag_frame.grid(row=1, column=2, rowspan=4, padx=8, pady=5, sticky="nw")
        tag_label.pack(side="top", anchor="w")
        tag_list.pack(side="top", anchor="w")
        tag_entry.pack(side="top", anchor="w", pady=(8, 2))
        add_tag.pack(side="top", anchor="w")

        submit.grid(row=5, column=3, padx=8, pady=8, sticky="se")

        window.mainloop()

    def choicewindow(self) -> None:
        choicew = tk.Tk()
        choicew.title("File Sorter v0.3")
        choicew.geometry("900x500")

        for row in range(6):
            choicew.rowconfigure(row, weight=1)
        for col in range(4):
            choicew.columnconfigure(col, weight=1)

        button_frame = tk.Frame(choicew)

        welcome = tk.Label(
            choicew,
            text="Pick which function you would like to use"
        )

        sortwindow = tk.Button(
            button_frame,
            text="File Sorter",
            padx=15,
            pady=3,
            command= lambda: self.makemainwindow(),
        )

        findwindow = tk.Button(
            button_frame,
            text="File Finder",
            padx=15,
            pady=3,
            command= lambda: sortGUI.makewindow(sortGUI()),
        )

        welcome.grid(row=0, column=0, columnspan=4, pady=8, sticky="w")

        button_frame.grid(
            row=1,
            column=0,
            rowspan=4,
            padx=8,
            pady=5,
            sticky="nw")
        sortwindow.pack(side="top", anchor="e")
        findwindow.pack(side="top", anchor="w")

        choicew.mainloop()



def main() -> None:
    window = GUI()
    window.choicewindow()


if __name__ == "__main__":
    main()
