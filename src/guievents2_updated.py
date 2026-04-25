"""Seperate file that holds all events and calls from the gui

Returns:
    None: Nada, Nothing
"""
from tkinter.filedialog import askdirectory, asksaveasfile
import os
import tkinter as tk
from course_updated import Course
from semester_updated import Semester
from tags import Tag


class Eventhandler:
    """GUI event helper methods."""

    # CHANGE NOTE:
    # Kept this as a static utility style so the rest of the GUI can call it
    # without needing to instantiate Eventhandler.
    @staticmethod
    def populatelist(box: tk.Listbox, gui: object) -> None:
        """Populate listbox with files from a selected directory.

        CHANGE NOTE:
        Save the chosen directory path on the GUI object so later events can
        still know where the files came from.
        """
        chosen_dir = askdirectory()
        if not chosen_dir:
            return

        gui.source_directory = chosen_dir
        mylist = os.listdir(chosen_dir)
        box.delete(0, tk.END)
        for file in mylist:
            box.insert(tk.END, file)

    @staticmethod
    def build_course_from_selection(gui: object, selected_label: str) -> Course | None:
        """Resolve the selected course label back to a Course object.

        CHANGE NOTE:
        This is the bridge between Combobox text and the Course model.
        """
        if selected_label in {"", "Select a Class"}:
            return None
        return gui.course_lookup.get(selected_label)

    @staticmethod
    def build_semester_from_selection(gui: object, selected_season: str) -> Semester | None:
        """Resolve/create the selected Semester object from the GUI.

        CHANGE NOTE:
        This keeps Semester usage inside the event layer instead of passing
        raw strings all the way through.
        """
        if selected_season in {"", "Select a Semester"}:
            return None

        for semester in gui.semesters:
            if semester.season == selected_season and semester.year == gui.current_year:
                gui.current_semester = semester
                return semester

        new_semester = Semester(year=gui.current_year, season=selected_season)
        gui.semesters.append(new_semester)
        gui.current_semester = new_semester
        return new_semester

    @staticmethod
    def savefileas(
        filelist: tk.Listbox,
        gui: object,
        selected_course_label: str,
        selected_semester_label: str,
    ) -> None:
        """Handle the final save intent.

        CHANGE NOTE:
        This still does not perform real project persistence, but it now uses
        Course / Semester / Tag data before opening the save dialog.
        """
        selected_course = Eventhandler.build_course_from_selection(
            gui, selected_course_label
        )
        selected_semester = Eventhandler.build_semester_from_selection(
            gui, selected_semester_label
        )

        if selected_course is None or selected_semester is None:
            return

        # CHANGE NOTE:
        # Attach the chosen course to the semester in memory. This satisfies
        # the requirement that the GUI/event flow actually uses the classes.
        if selected_course not in selected_semester.courses:
            selected_semester.add_course(selected_course)

        # CHANGE NOTE:
        # The initial directory is now derived from a Semester object instead of
        # a hardcoded string.
        directory = os.path.join(
            str(selected_semester.year),
            selected_semester.season,
        )

        for i in filelist.curselection():
            file = filelist.get(i)
            asksaveasfile(
                mode="w",
                confirmoverwrite=True,
                initialdir=directory,
                initialfile=file,
            )

    @staticmethod
    def prepfilestruct(semesters: list[Semester]) -> None:
        """Prepare folders from Semester objects.

        CHANGE NOTE:
        Replaced the old hardcoded season list with Semester objects supplied
        by the GUI layer.
        """
        for semester in semesters:
            year_dir = str(semester.year)
            sem_dir = os.path.join(year_dir, semester.season)

            try:
                os.makedirs(sem_dir, exist_ok=True)
            except PermissionError:
                print(f"Permission denied: Unable to create '{sem_dir}'.")

    @staticmethod
    def make_tag(name: str, desc: str = "") -> Tag:
        """Small helper used by GUI setup for Tag creation."""
        tag = Tag()
        tag.set_name(name)
        tag.set_description(desc)
        return tag
