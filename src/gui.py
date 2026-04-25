"""Main Program
   Updated with the help of ChatGPT
"""
import tkinter as tk
from tkinter import ttk as tkk
import typing
from typing import Optional
from guievents2 import Eventhandler
from directory_model import DirectoryModel as DM, os
import subprocess


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
        self.classoptions = ["Math", "English", "Labs", "ComputerScience"]
        self.semester = ["Fall", "J-term", "Spring", "Summer"]

        self.selected_year = ""
        self.selected_semester = ""
        self.selected_class = ""
        self.current_class_path = ""

        self.dir_model = DM()

        self.yeardropdown = None
        self.semdropdown = None
        self.classdropdown = None
        self.classitemsbox = None

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
        yeardropdownframe = tk.Frame(window)  # paired Semdropdown and label
        semdropdownframe = tk.Frame(window)  # paired Semdropdown and label
        classdropdownframe = tk.Frame(window)  # paired Tagdropdown and label
        classitemsframe = tk.Frame(window)  # listbox for class directory

        # year dropdown
        self.yeardropdown = tkk.Combobox(yeardropdownframe,
                                   values=years,
                                   state="readonly",
                                   width=20
                                   )

        # sem dropdown
        self.semdropdown = tkk.Combobox(semdropdownframe,
                                   values=[],
                                   state="readonly",
                                   width=20
                                   )

        # class dropdown
        self.classdropdown = tkk.Combobox(classdropdownframe,
                                   values=[],
                                   state="readonly",
                                   width=20
                                   )

        # class file listbox
        self.classitemsbox = tk.Listbox(classitemsframe,
                                selectmode="single",
                                width=30,
                                height=10
                                )

        # scrollbar for classitem listbox
        classscrollbar = tk.Scrollbar(classitemsframe,
                                orient="vertical",
                                command=self.classitemsbox.yview
                                )
        self.classitemsbox.config(yscrollcommand=classscrollbar.set)

        # up button (move up the dir)
        self.upbutton = tk.Button(classitemsframe,
                            text="../",
                            command=self.go_up_dir
                            )

        # set values for dropdown menus (with default)
        if current_year in years:
            self.yeardropdown.set(current_year)
        else:
            self.yeardropdown.set("Select a year")

        self.update_semesters()

        # bind the values
        self.yeardropdown.bind("<<ComboboxSelected>>", self.update_semesters)
        self.semdropdown.bind("<<ComboboxSelected>>", self.update_classes)
        self.classdropdown.bind("<<ComboboxSelected>>", self.update_class_items)
        self.classitemsbox.bind("<Double-1>", self.open_selected_item)

        # update pack calls
        self.yeardropdown.pack(side="bottom")
        self.semdropdown.pack(side="bottom")
        self.classdropdown.pack(side="bottom")

        # save button
        submit = tk.Button(window,
                           text="Save file",
                           anchor="se",
                           padx=20,  # size of button in x
                           pady=3  # size of button in y
                           )

        # intro text on win
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

        classitemslabel = tk.Label(classitemsframe,
                            text="Files in selected class")

        # top message
        spacer.grid(row=0, column=0, pady=3, sticky="w")

        # year section below title
        yeardropdownframe.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        yearlabel.pack(side="top")

        # sem section below year
        semdropdownframe.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        semlabel.pack(side="top")

        # class section below semester
        classdropdownframe.grid(row=3, column=0, padx=30, pady=5, sticky="w")
        self.classdropdown.pack(side="bottom")
        classlabel.pack(side="top")

        # packing
        self.upbutton.pack(side="top")
        classitemsframe.grid(row=4, column=0, padx=90, pady=5, sticky="w")
        classitemslabel.pack(side="top")
        self.classitemsbox.pack(side="left", fill="y")
        classscrollbar.pack(side="right", fill="y")

        #lower right save button
        submit.grid(row=5, column=5, padx=30, pady=5, sticky="se")

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

    def load_class_items(self, year: str, semester: str, classname: str) -> list[str]:
        """Loads files and directories from a class directory."""
        return self.dir_model.get_items(f"CMU/{year}/{semester}/{classname}")

    def update_semesters(self, event=None) -> None:
        year = self.yeardropdown.get()
        self.selected_year = year

        semesters = self.load_semesters(year)
        self.semdropdown["values"] = semesters

        current_semester = self.dir_model.get_current_semester()
        if current_semester in semesters:
            self.semdropdown.set(current_semester)
            self.selected_semester = current_semester
        elif semesters:
            self.semdropdown.set(semesters[0])
            self.selected_semester = semesters[0]
        else:
            self.semdropdown.set("Select a Semester")
            self.selected_semester = ""

        self.update_classes()
        self.update_class_items()

    def update_classes(self, event=None) -> None:
        year = self.yeardropdown.get()
        semester = self.semdropdown.get()

        classes = self.load_classes(year, semester)
        self.classdropdown["values"] = classes

        if classes:
            classname = classes[0]
            self.classdropdown.set(classname)
            self.selected_class = classname
            self.current_class_path = os.path.join("CMU", year, semester, classname)
        else:
            self.classdropdown.set("Select a Class")
            self.selected_class = ""
            self.current_class_path = ""

        self.update_class_items()

    def update_class_items(self, event=None) -> None:
        self.classitemsbox.delete(0, tk.END)

        year = self.yeardropdown.get()
        semester = self.semdropdown.get()
        classname = self.classdropdown.get()

        if year == "Select a year" or not year:
            self.current_class_path = ""
            return
        if semester == "Select a Semester" or not semester:
            self.current_class_path = ""
            return
        if classname == "Select a Class" or not classname:
            self.current_class_path = ""
            return

        class_root = os.path.join("CMU", year, semester, classname)

        if not self.current_class_path:
            self.current_class_path = class_root

        items = self.dir_model.get_items(self.current_class_path)

        for item in items:
            full_path = os.path.join(self.current_class_path, item)
            if os.path.isdir(full_path):
                self.classitemsbox.insert(tk.END, f"{item}/")
            else:
                self.classitemsbox.insert(tk.END, item)

    def open_selected_item(self, event=None) -> None:
        selection = self.classitemsbox.curselection()
        if not selection:
            return

        name = self.classitemsbox.get(selection[0]).rstrip("/")
        next_path = os.path.join(self.current_class_path, name)

        if os.path.isdir(next_path):
            self.current_class_path = next_path
            self.update_class_items()
        else:
            subprocess.run(["xdg-open", next_path], check=False)

    def go_up_dir(self) -> None:
        if not self.current_class_path:
            return

        parent = os.path.dirname(self.current_class_path)

        # prevent going above the selected class root if you want
        class_root = os.path.join(
            "CMU",
            self.yeardropdown.get(),
            self.semdropdown.get(),
            self.classdropdown.get()
        )

        if os.path.normpath(self.current_class_path) == os.path.normpath(class_root):
            return

        self.current_class_path = parent
        self.update_class_items()


def main():
    Eventhandler.prepfilestruct(())
    window = GUI()
    window.makewindow()


if __name__ == "__main__":
    main()
# add constraints to what can be input
# entry/ add error catching for invalid entries
# add scrollbar that works
