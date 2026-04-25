"""main program file"""
import tkinter as tk
from tkinter import ttk as tkk
import typing
from typing import Optional
from guievents2_updated import Eventhandler
from course_updated import Course
from semester_updated import Semester


class GUI:
    _instance: Optional["GUI"] = None

    def __new__(
        cls,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[typing.Any, typing.Any],
    ) -> "GUI":
        """Creates a new instance of the class if not already created."""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # CHANGE NOTE:
        # Guard __init__ because Singleton + repeated GUI() calls would
        # otherwise rebuild all state.
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        # CHANGE NOTE:
        # Store real Tag objects instead of plain strings.
        self.tags = [
            Eventhandler.make_tag("MATH", "Math department"),
            Eventhandler.make_tag("ENGL", "English department"),
            Eventhandler.make_tag("LABS", "Lab course tag"),
            Eventhandler.make_tag("CSCI", "Computer Science department"),
        ]

        # CHANGE NOTE:
        # Store real Course objects so the class dropdown can represent the
        # Course model instead of a text-only placeholder.
        self.courses = [
            Course("Discrete Structures", 145, self.tags[3]),
            Course("Composition", 150, self.tags[1]),
            Course("Calculus", 151, self.tags[0]),
        ]
        self.course_lookup = {str(course): course for course in self.courses}
        self.course_options = list(self.course_lookup.keys())

        # CHANGE NOTE:
        # Keep all created Semester objects plus a currently selected one.
        self.current_year = 2026
        self.semesters = [
            Semester(year=self.current_year, season="Fall"),
            Semester(year=self.current_year, season="J-term"),
            Semester(year=self.current_year, season="Spring"),
            Semester(year=self.current_year, season="Summer"),
        ]
        self.current_semester: Semester | None = None
        self.semester_options = [semester.season for semester in self.semesters]

        # CHANGE NOTE:
        # Remember where the user selected files from.
        self.source_directory = ""

    def makewindow(self) -> None:
        window = tk.Tk()
        window.title("File Sorter v0.2")
        window.geometry("900x500+30+30")
        for row in range(5):
            window.rowconfigure(row, weight=1)
        for col in range(5):
            window.columnconfigure(col, weight=1)
        window.rowconfigure(0, weight=0)
        window.rowconfigure(2, weight=0)
        listboxframe = tk.Frame(window)
        tagdropdownframe = tk.Frame(window)
        semdropdownframe = tk.Frame(window)

        filelist = tk.Listbox(
            listboxframe,
            selectmode="multiple",
            width=30,
            height=10,
        )

        dirpick = tk.Button(
            listboxframe,
            text="Pick Directory",
            anchor="ne",
            padx=15,
            pady=3,
        )
        dirpick.bind(
            "<Button-1>",
            lambda event: Eventhandler.populatelist(filelist, self),
        )

        # CHANGE NOTE:
        # This dropdown now represents Course objects via their string labels.
        classdropdown = tkk.Combobox(
            tagdropdownframe,
            values=self.course_options,
            state="readonly",
            width=30,
        )
        classdropdown.set("Select a Class")

        # CHANGE NOTE:
        # This dropdown is backed by Semester objects through season labels.
        semdropdown = tkk.Combobox(
            semdropdownframe,
            values=self.semester_options,
            state="readonly",
            width=20,
        )
        semdropdown.set("Select a Semester")

        submit = tk.Button(
            window,
            text="Save file",
            anchor="se",
            padx=20,
            pady=3,
        )
        submit.bind(
            "<Button-1>",
            lambda event: Eventhandler.savefileas(
                filelist,
                self,
                classdropdown.get(),
                semdropdown.get(),
            ),
        )
        spacer = tk.Label(
            window,
            text="Welcome to the File Sorter! To start with pick your messy directory",
        )

        classlabel = tk.Label(
            tagdropdownframe,
            text="Pick your class",
        )

        semlabel = tk.Label(
            semdropdownframe,
            text="Pick your semester",
        )

        scrollbar = tk.Scrollbar(
            listboxframe,
            orient="vertical",
            command=filelist.yview,
        )
        filelist.config(yscrollcommand=scrollbar.set)

        spacer.grid(row=0, column=0, pady=3, sticky="w")
        listboxframe.grid(row=1, column=0, sticky="w")
        dirpick.pack(side="top")
        filelist.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")
        tagdropdownframe.grid(row=2, column=0, padx=3, pady=5, sticky="w")
        classdropdown.pack(side="bottom")
        classlabel.pack(side="top")
        semdropdownframe.grid(row=3, column=0, padx=3, pady=5, sticky="w")
        semdropdown.pack(side="bottom")
        semlabel.pack(side="top")
        submit.grid(row=5, column=5, padx=3, pady=5, sticky="se")
        window.mainloop()


def main() -> None:
    window = GUI()
    Eventhandler.prepfilestruct(window.semesters)
    window.makewindow()


if __name__ == "__main__":
    main()
