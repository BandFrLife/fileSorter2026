"""main program file
"""
import re
import tkinter as tk
import typing
from tkinter import ttk as tkk
from typing import Optional
from pathlib import Path
from guievents import Eventhandler
from semester import Semester
from course import Course
from tags import Tag


class GUI ():
    _instance: Optional["GUI"] = None

    SEMESTERS = ["Fall", "J-term", "Spring", "Summer"]

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
        """ Setups up attributes for the gui window.
            Gathers up-to-date information of files,
            directories, and current status.
        """
        self.project_root = Path(__file__).resolve().parent.parent
        self.cmu_root = self.project_root / "CMU"

        if self.dir_empty():
            Eventhandler.prepfilestruct(())

        self.tagoptions = []
        self.semester = self.get_semesters()
        self.years = []
        self.classes: list[[str],[str]] = []

        self.current_year = str(Eventhandler.get_current_year(self))
        self.current_semester = Eventhandler.get_current_semester(self)
        self.window = None
        #self.listboxframe = None
        self.classboxframe = None

        self.classbox = None
        self.classscrollbar = None
        self.upbutton = None
        self.current_class_path = ""
        self.classitemsbox = None

        self.dirdropdownframe = None
        self.semdropdownframe = None

        #self.filelist = None
        self.dirdropdown = None
        self.semdropdown = None
        #self.submit = None
        self.spacer = None
        self.dirlabel = None
        self.semlabel = None
        self.classlabel = None
        classdropdownlabel = None
        classboxlabel = None

    def makewindow(self):
        """Creates and updates everything related to the output window."""
        window = tk.Tk()
        window.title("File Sorter v0.2")

        window.geometry('900x500+30+30')  # window size(x,y), offest
        for row in range(5):
            window.rowconfigure(row, weight=1)
        for col in range(5):
            window.columnconfigure(col, weight=1)
        window.rowconfigure(0, weight=0)
        window.rowconfigure(2, weight=0)

        self.dirdropdownframe = tk.Frame(window)  # for scrollable listbox
        self.semdropdownframe = tk.Frame(window)  # for paired Semdropdown and label
        self.classdropdownframe = tk.Frame(window) # for paired classdropdown and label

        self.dirdropdown = tkk.Combobox(self.dirdropdownframe,
                                   values=self.get_years(),
                                   state="readonly",
                                   width=20
                                   )
        self.dirdropdown.set(self.current_year)
        self.dirdropdown.bind("<<ComboboxSelected>>", self.update_semesters)

        self.semdropdown = tkk.Combobox(self.semdropdownframe,
                                   values=[],
                                   state="readonly",
                                   width=20
                                   )
        self.semdropdown.set(self.current_semester)
        self.semdropdown.bind("<<ComboboxSelected>>", self.update_classes)


        self.classboxframe = tk.Frame(window)

        self.classbox = tk.Listbox(
            self.classboxframe,
            selectmode="single",
            width=30,
            height=10
        )

        self.upbutton = tk.Button(
            self.classboxframe,
            text="../",
            command=self.go_up_dir
        )

        self.classbox.bind("<Double-1>", self.open_selected_item)

        self.classdropdown = tkk.Combobox(self.classdropdownframe,
                                   values=self.tagoptions,
                                   state="readonly",
                                   width=20
                                   )
        self.classdropdown.set("Select a Class")

        self.classboxframe = tk.Frame(window)

        self.classbox = tk.Listbox(
            self.classboxframe,
            selectmode="single",
            width=30,
            height=10
        )

        self.classscrollbar = tk.Scrollbar(
            self.classboxframe,
            orient="vertical",
            command=self.classbox.yview
        )

        self.classbox.config(yscrollcommand=self.classscrollbar.set)

        self.upbutton = tk.Button(
            self.classboxframe,
            text="../",
            command=self.go_up_dir
        )

        self.classbox.bind("<Double-1>", self.open_selected_item)
        self.classdropdown.bind("<<ComboboxSelected>>", self.update_class_items)
        self.init_dropdowns()

        #submit = tk.Button(window,
        #                   text="Save file",
        #                   anchor="se",
        #                   padx=20,  # size of button in x
        #                   pady=3  # size of button in y
        #                   )
        #submit.bind('<Button-1>', lambda event: Eventhandler.savefileas
        #            ((), filelist, ("2026/"+self.semdropdown.get())))
        spacer = tk.Label(window,
                          text="Welcome to the File Sorter! "
                          "To start with pick your messy directory")

        dirlabel = tk.Label(self.dirdropdownframe,
                            text="Pick your year")

        semlabel = tk.Label(self.semdropdownframe,
                            text="Pick your semester")

        classlabel = tk.Label(self.classboxframe,
                              text="Pick your class")

        classdropdownlabel = tk.Label(self.classdropdownframe,
                                      text="Pick your class")

        classboxlabel = tk.Label(self.classboxframe,
                                 text="Class contents")

#       Building the window, order matters
        spacer.grid(row=0, column=0, pady=3, sticky="w")
        #listboxframe.grid(row=1, column=0, sticky="w")
        self.dirdropdown.pack(side="top")
        #filelist.pack(side="left", fill="y")

        self.dirdropdownframe.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        self.dirdropdown.pack(side="bottom")
        dirlabel.pack(side="top")

        self.semdropdownframe.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        self.semdropdown.pack(side="bottom")
        semlabel.pack(side="top")

        self.classdropdownframe.grid(row=3, column=0, padx=30, pady=5, sticky="w")
        classdropdownlabel.pack(side="top")
        self.classdropdown.pack(side="bottom")

        self.classboxframe.grid(row=4, column=0, padx=30, pady=5, sticky="w")
        classlabel.pack(side="top")
        self.upbutton.pack(side="top")
        self.classbox.pack(side="left", fill="y")
        self.classscrollbar.pack(side="right", fill="y")

        #submit.grid(row=5, column=5, padx=3, pady=5, sticky="se")
        window.mainloop()

    def scan_dir(self) -> tuple[list[Path],list[str]]:
        """ Recursively finds all files and directories inside CMU.
            Returns a list of Path objects.

        Returns:
            tuple[list[Path],list[str]]: (list of directories, list of files)
        """
        if not self.cmu_root.exists():
            return []

        data = list(self.cmu_root.rglob("*"))

        files = []
        dirs = []

        for item in data:
            if item.is_dir():
                dirs.append(item)
            elif item.is_file():
                files.append(str(item))

        return (dirs,files)

    def dir_empty(self) -> bool:
        """Check if a directory is empty.

        Returns:
            bool: True if no present dirs, False if dirs present.
        """
        directories, _ = self.scan_dir()
        return not directories

    def get_semesters(self) -> list[Semester]:
        """Check root directory recursively for subdirectories.
           Includes only semesters directories.

        Returns:
            list[Semester]: list of all semesters found.
        """
        semesters = []

        for year_dir in self.cmu_root.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue

            year = int(year_dir.name)

            for sem_dir in year_dir.iterdir():
                if not sem_dir.is_dir():
                    continue

                courses = []

                for course_dir in sem_dir.iterdir():
                    if not course_dir.is_dir():
                        continue

                    valid = re.fullmatch(r"([A-Z]{4})(\d{3})", course_dir.name)
                    if valid:
                        tag = Tag(name=valid.group(1))
                        course = Course(course_dir.name, int(valid.group(2)), tag)
                        courses.append(course)

                semesters.append(
                    Semester(
                        year=year,
                        semester=sem_dir.name,
                        courses=courses,
                        path=str(sem_dir)))

        return semesters

    def get_years(self) -> list[str]:
        """Check root directory recursively for subdirectories.
           Includes only year directories.

        Returns:
            list[str]: list of all year directories found.
        """
        dirs, _ = self.scan_dir()
        dirs.sort()
        years = []

        for d in dirs:
            try:
                int(d.name)
                years.append(d.name)
            except:
                pass

        return years


    def init_dropdowns(self) -> None:
        """Initialize the dropdown boxes.
        """
        years = self.get_years()

        #self.dirdropdown["values"] = years

        if self.current_year in years:
            self.dirdropdown.set(self.current_year)
        elif years:
            self.dirdropdown.set(years[0])
        else:
            #self.dirdropdown.set("Pick a year")
            return

        self.update_semesters(initial=True)

    def update_semesters(self, event=None, initial: bool = False) -> None:
        """Updates the dropdown lists for semester."""
        year = self.dirdropdown.get()
        semesters = [
            sem.semester
            for sem in self.semester
            if str(sem.year) == str(year)
        ]

        self.semdropdown["values"] = semesters

        if initial and self.current_semester in semesters:
            self.semdropdown.set(self.current_semester)
        elif semesters:
            self.semdropdown.set(semesters[0])
        else:
            self.semdropdown.set("Pick a semester")
            return

        self.update_classes()

    def update_classes(self, event=None) -> None:
        year = self.dirdropdown.get()
        semester = self.semdropdown.get()

        classes = []

        for sem in self.semester:
            if str(sem.year) == str(year) and sem.semester == semester:
                classes = [str(course) for course in sem.courses]
                break

        self.classdropdown["values"] = classes
        self.classdropdown.set("Pick a class")

        self.current_class_path = ""
        self.classbox.delete(0, tk.END)

    def open_selected_item(self, event=None) -> None:
        selection = self.classbox.curselection()
        if not selection:
            return

        name = self.classbox.get(selection[0]).rstrip("/")
        next_path = Path(self.current_class_path) / name

        if next_path.is_dir():
            self.current_class_path = str(next_path)
            self.refresh_classbox()

    def refresh_classbox(self) -> None:
        self.classbox.delete(0, tk.END)

        if not self.current_class_path:
            return

        for item in Path(self.current_class_path).iterdir():
            if item.is_dir():
                self.classbox.insert(tk.END, f"{item.name}/")
            else:
                self.classbox.insert(tk.END, item.name)

    def go_up_dir(self) -> None:
        if not self.current_class_path:
            return

        current = Path(self.current_class_path)
        parent = current.parent

        year = self.dirdropdown.get()
        semester = self.semdropdown.get()
        semester_root = self.cmu_root / year / semester

        if current == semester_root:
            return

        self.current_class_path = str(parent)
        self.refresh_classbox()

    def update_class_items(self, event=None) -> None:
        year = self.dirdropdown.get()
        semester = self.semdropdown.get()
        classname = self.classdropdown.get()

        if classname == "Pick a class":
            return

        self.current_class_path = self.cmu_root / year / semester / classname
        self.refresh_classbox()

    def refresh_class_items(self) -> None:
        self.classitemsbox.delete(0, tk.END)

        for item in os.listdir(self.current_class_path):
            full_path = os.path.join(self.current_class_path, item)

            if os.path.isdir(full_path):
                self.classitemsbox.insert(tk.END, f"{item}/")
            else:
                self.classitemsbox.insert(tk.END, item)

    def add_class(self) -> None:
        """Adds a new class directory to a semester directory."""
        pass

    def add_tag(self) -> None:
        """Adds a new tag to class attribute self.tagoptions."""
        pass

    @staticmethod
    def main():
        """Entry static method."""
        window = GUI()
        window.makewindow()


if __name__ == "__main__": # pragma: no cover
    GUI.main()
# add constraints to what can be input
# entry/ add error catching for invalid entries
