"""main program file
"""
import re
import tkinter as tk
import typing
from tkinter import ttk as tkk
from tkinter import messagebox
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
        self.classes: list[[str], [str]] = []

        self.current_year = str(Eventhandler.get_current_year(self))
        self.current_semester = Eventhandler.get_current_semester(self)
        self.window = None
        # self.listboxframe = None
        self.classboxframe = None

        self.classbox = None
        self.classscrollbar = None
        self.upbutton = None
        self.current_class_path = ""
        self.classitemsbox = None

        self.yeardropdownframe = None
        self.semdropdownframe = None

        # self.filelist = None
        self.yeardropdown = None
        self.semdropdown = None
        # self.submit = None
        self.spacer = None
        self.yearlabel = None
        self.semlabel = None
        self.classlabel = None
        self.classdropdownlabel = None
        self.classboxlabel = None

        self.addyearbutton = None
        # self.addsemesterbutton = None
        self.addclassbutton = None

        self.createfilebutton = None
        self.createfolderbutton = None

    def makewindow(self):
        """Creates and updates everything related to the output window."""
        window = tk.Tk()
        window.title("File Sorter v2.0")

        window.geometry('900x500+30+30')  # window size(x,y), offest

        for row in range(5):
            window.rowconfigure(row, weight=0)

        window.rowconfigure(4, weight=1)
        window.columnconfigure(0, weight=1)

        self.yeardropdownframe = tk.Frame(window)  # for scrollable listbox
        # for paired Semdropdown and label
        self.semdropdownframe = tk.Frame(window)
        # for paired classdropdown and label
        self.classdropdownframe = tk.Frame(window)

        self.yeardropdown = tkk.Combobox(self.yeardropdownframe,
                                         values=self.get_years(),
                                         state="readonly",
                                         width=20
                                         )
        self.yeardropdown.set(self.current_year)
        self.yeardropdown.bind("<<ComboboxSelected>>", self.update_semesters)

        self.semdropdown = tkk.Combobox(self.semdropdownframe,
                                        values=[],
                                        state="readonly",
                                        width=20
                                        )
        self.semdropdown.set(self.current_semester)
        self.semdropdown.bind("<<ComboboxSelected>>", self.update_classes)

        self.classdropdown = tkk.Combobox(self.classdropdownframe,
                                          values=self.tagoptions,
                                          state="readonly",
                                          width=20
                                          )
        self.classdropdown.set("Select a Class")

        self.classboxframe = tk.Frame(window)
        self.classboxframe.columnconfigure(0, weight=1)
        self.classboxframe.rowconfigure(2, weight=1)

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

        self.createfilebutton = tk.Button(
            self.classboxframe,
            text="Create file",
            command=self.create_file
        )

        self.createfolderbutton = tk.Button(
            self.classboxframe,
            text="Create folder",
            command=self.create_folder
        )

        self.classbox.bind("<Double-1>", self.open_selected_item)

        self.classbox.config(yscrollcommand=self.classscrollbar.set)

        self.addyearbutton = tk.Button(
            self.yeardropdownframe,
            text="Add year",
            command=self.add_year
        )

        # self.addsemesterbutton = tk.Button(
        #     self.semdropdownframe,
        #     text="Add semester",
        #     command=self.add_semester
        # )

        self.addclassbutton = tk.Button(
            self.classdropdownframe,
            text="Add class",
            command=self.add_class
        )

        self.classbox.bind("<Double-1>", self.open_selected_item)
        self.classdropdown.bind(
            "<<ComboboxSelected>>",
            self.update_class_items)
        self.init_dropdowns()

        # submit = tk.Button(window,
        #                    text="Save file",
        #                    anchor="se",
        #                    padx=20,  #  size of button in x
        #                    pady=3  #   size of button in y
        #                     )
        #  submit.bind('<Button-1>', lambda event: Eventhandler.savefileas
        #              ((), filelist, ("2026/"+self.semdropdown.get())))
        spacer = tk.Label(
            window,
            text="Welcome to the School File Sorter!"
        )

        yearlabel = tk.Label(
            self.yeardropdownframe,
            text="Pick your year",
            anchor="w"
        )

        semlabel = tk.Label(
            self.semdropdownframe,
            text="Pick your semester",
            anchor="w"
        )

        classlabel = tk.Label(
            self.classboxframe,
            text="Pick your class",
            anchor="w"
        )

        self.classdropdownlabel = tk.Label(
            self.classdropdownframe,
            text="Pick your class",
            anchor="w"
        )

        self.classboxlabel = tk.Label(
            self.classboxframe,
            text="Class contents",
            anchor="w"
        )

#       Building the window, order matters
        spacer.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.yeardropdownframe.grid(
            row=1, column=0, padx=30, pady=5, sticky="w")
        yearlabel.pack(side="top", anchor="w", fill="x")
        self.yeardropdown.pack(side="left", padx=(0, 10))
        self.addyearbutton.pack(side="left")

        self.semdropdownframe.grid(
            row=2, column=0, padx=30, pady=5, sticky="w")
        semlabel.pack(side="top", anchor="w", fill="x")
        self.semdropdown.pack(side="left", padx=(0, 10))
        # self.addsemesterbutton.pack(side="left")

        self.classdropdownframe.grid(
            row=3, column=0, padx=30, pady=5, sticky="w")
        self.classdropdownlabel.pack(side="top", anchor="w", fill="x")
        self.classdropdown.pack(side="left", padx=(0, 5))
        self.addclassbutton.pack(side="left")

        self.classboxframe.grid(
            row=4, column=0, padx=30, pady=(
                5, 30), sticky="nsew")

        classlabel.grid(row=0, column=0, columnspan=2, sticky="w")
        self.upbutton.grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.createfilebutton.grid(
            row=1, column=0, sticky="w", padx=(
                45, 0), pady=(
                0, 5))
        self.createfolderbutton.grid(
            row=1, column=0, sticky="w", padx=(
                140, 0), pady=(
                0, 5))

        self.classbox.grid(row=2, column=0, sticky="nsew")
        self.classscrollbar.grid(row=2, column=1, sticky="ns")

        # submit.grid(row=5, column=5, padx=3, pady=5, sticky="se")
        window.mainloop()

    def scan_dir(self) -> tuple[list[Path], list[str]]:
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

        return (dirs, files)

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
                        course = Course(
                            course_dir.name, int(
                                valid.group(2)), tag)
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
            except BaseException:
                pass

        return years

    def init_dropdowns(self) -> None:
        """Initialize the dropdown boxes.
        """
        years = self.get_years()

        # self.yeardropdown["values"] = years

        if self.current_year in years:
            self.yeardropdown.set(self.current_year)
        elif years:
            self.yeardropdown.set(years[0])
        else:
            # self.yeardropdown.set("Pick a year")
            return

        self.update_semesters(initial=True)

    def update_semesters(self, event=None, initial: bool = False) -> None:
        """Updates the dropdown lists for semester."""
        year = self.yeardropdown.get()
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
        year = self.yeardropdown.get()
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

        year = self.yeardropdown.get()
        semester = self.semdropdown.get()
        classname = self.classdropdown.get()

        if classname == "Pick a class":
            return

        current = Path(self.current_class_path)
        class_root = self.cmu_root / year / semester / classname

        if current == class_root:
            return

        self.current_class_path = str(current.parent)
        self.refresh_classbox()

    def update_class_items(self, event=None) -> None:
        year = self.yeardropdown.get()
        semester = self.semdropdown.get()
        classname = self.classdropdown.get()

        if classname == "Pick a class":
            return

        self.current_class_path = self.cmu_root / year / semester / classname
        self.refresh_classbox()

    def add_popup(self, title: str, label: str, save_command) -> None:
        """Creates a small popup with an entry and save button."""
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("300x120")

        entry_label = tk.Label(popup, text=label)
        entry_label.pack(pady=5)

        entry = tk.Entry(popup, width=25)
        entry.pack(pady=5)
        entry.focus()

        def save() -> None:
            value = entry.get().strip()
            if not value:
                messagebox.showerror("Error", "Input cannot be empty.")
                return

            save_command(value)
            popup.destroy()

        save_button = tk.Button(popup, text="Save", command=save)
        save_button.pack(pady=5)

    def add_year(self) -> None:
        """Adds a new year directory under CMU."""
        self.add_popup("Add Year", "Enter year, example: 2030", self.save_year)

    def save_year(self, year: str) -> None:
        if not year.isdigit() or len(year) != 4:
            messagebox.showerror("Error", "Year must be 4 digits.")
            return

        year_path = self.cmu_root / year
        year_path.mkdir(exist_ok=True)

        for semester in self.SEMESTERS:
            (year_path / semester).mkdir(exist_ok=True)

        self.semester = self.get_semesters()
        self.yeardropdown["values"] = self.get_years()
        self.yeardropdown.set(year)
        self.update_semesters()

    def add_semester(self) -> None:
        """Adds a new semester directory under selected year."""
        self.add_popup(
            "Add Semester",
            "Enter semester: Fall, J-term, Spring, Summer",
            self.save_semester
        )

    def save_semester(self, semester: str) -> None:
        year = self.yeardropdown.get()

        if semester not in self.SEMESTERS:
            messagebox.showerror(
                "Error",
                "Semester must be Fall, J-term, Spring, or Summer."
            )
            return

        semester_path = self.cmu_root / year / semester
        semester_path.mkdir(parents=True, exist_ok=True)

        self.semester = self.get_semesters()
        self.update_semesters()
        self.semdropdown.set(semester)
        self.update_classes()

    def add_class(self) -> None:
        """Adds a new class directory to selected year/semester."""
        self.add_popup(
            "Add Class",
            "Enter class, example: CSCI111",
            self.save_class
        )

    def save_class(self, classname: str) -> None:
        year = self.yeardropdown.get()
        semester = self.semdropdown.get()

        valid = re.fullmatch(r"[A-Z]{4}\d{3}", classname)

        if not valid:
            messagebox.showerror(
                "Error",
                "Class must match format AAAA111, example: CSCI111."
            )
            return

        class_path = self.cmu_root / year / semester / classname
        class_path.mkdir(parents=True, exist_ok=True)

        self.semester = self.get_semesters()
        self.update_classes()
        self.classdropdown.set(classname)
        self.update_class_items()

    def create_file(self) -> None:
        """Creates a file in the currently viewed class/folder."""
        self.add_popup("Create File", "Enter file name", self.save_file)

    def save_file(self, filename: str) -> None:
        if not self.current_class_path:
            messagebox.showerror("Error", "Pick a class first.")
            return

        file_path = Path(self.current_class_path) / filename

        if file_path.exists():
            messagebox.showerror("Error", "File already exists.")
            return

        file_path.touch()
        self.refresh_classbox()

    def create_folder(self) -> None:
        """Creates a folder in the currently viewed class/folder."""
        self.add_popup("Create Folder", "Enter folder name", self.save_folder)

    def save_folder(self, foldername: str) -> None:
        if not self.current_class_path:
            messagebox.showerror("Error", "Pick a class first.")
            return

        folder_path = Path(self.current_class_path) / foldername

        if folder_path.exists():
            messagebox.showerror("Error", "Folder already exists.")
            return

        folder_path.mkdir()
        self.refresh_classbox()

    def add_tag(self) -> None:
        """Adds a new tag to class attribute self.tagoptions."""
        pass

    @staticmethod
    def main():
        """Entry static method."""
        window = GUI()
        window.makewindow()


if __name__ == "__main__":  # pragma: no cover
    GUI.main()
# add constraints to what can be input
# entry/ add error catching for invalid entries
