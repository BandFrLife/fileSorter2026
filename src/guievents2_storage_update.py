"""Separate file that holds all events and storage helpers."""
from __future__ import annotations

from pathlib import Path
from tkinter.filedialog import askdirectory, asksaveasfile
import datetime
import os
import tkinter as tk

from course_updated import Course
from semester_updated import Semester
from tags import Tag


class Eventhandler:
    """GUI event helper methods."""

    SEASONS = ["Fall", "J-term", "Spring", "Summer"]

    @staticmethod
    def get_current_year() -> int:
        """Small helper so GUI setup does not hardcode the year."""
        return datetime.datetime.now().year

    @staticmethod
    def semester_label(semester: Semester) -> str:
        """Return a unique combobox label for a Semester."""
        return f"{semester.season} {semester.year}"

    @staticmethod
    def build_default_semesters(start_year: int) -> list[Semester]:
        """Build four years of Semester objects, starting with start_year.

        CHANGE NOTE:
        First-run storage now creates four years immediately instead of just
        one year.
        """
        semesters: list[Semester] = []
        for year in range(start_year, start_year + 4):
            for season in Eventhandler.SEASONS:
                semesters.append(Semester(year=year, season=season))
        return semesters

    @staticmethod
    def is_directory_effectively_empty(cmu_root: Path) -> bool:
        """Return True when CMU has no saved content yet.

        CHANGE NOTE:
        The first check is whether ./CMU contains anything meaningful.
        """
        if not cmu_root.exists():
            return True
        return not any(cmu_root.iterdir())

    @staticmethod
    def populate_gui_courses_from_state(gui: object, semesters: list[Semester]) -> None:
        """Merge any courses loaded from disk into the GUI course list.

        CHANGE NOTE:
        If the save file knows about courses that are not in the hardcoded GUI
        defaults, add them so the combobox can still display them.
        """
        for semester in semesters:
            for course in semester.courses:
                label = str(course)
                if label not in gui.course_lookup:
                    gui.courses.append(course)
                    gui.course_lookup[label] = course

        gui.course_options = list(gui.course_lookup.keys())

    @staticmethod
    def initialize_storage(gui: object) -> list[Semester]:
        """Initialize ./CMU state.

        Rules:
        - If ./CMU is empty, create four years of semester folders and a simple
          text state file.
        - If ./CMU is not empty, load from the state file and do not recreate
          or modify the existing folders.
        """
        gui.cmu_root.mkdir(parents=True, exist_ok=True)

        if Eventhandler.is_directory_effectively_empty(gui.cmu_root):
            semesters = Eventhandler.build_default_semesters(gui.current_year)
            Eventhandler.prepfilestruct(semesters, gui.cmu_root)
            Eventhandler.write_state_file(gui.save_file, semesters)
        else:
            semesters = Eventhandler.load_state_file(gui.save_file)
            # CHANGE NOTE:
            # The user asked to assume a .txt save file exists. This fallback
            # only keeps the GUI usable if the text file is missing.
            if not semesters:
                semesters = Eventhandler.scan_semesters_from_fs(gui.cmu_root)

        Eventhandler.populate_gui_courses_from_state(gui, semesters)
        return semesters

    @staticmethod
    def populatelist(box: tk.Listbox, gui: object) -> None:
        """Populate listbox with files from a selected directory."""
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
        """Resolve the selected course label back to a Course object."""
        if selected_label in {"", "Select a Class"}:
            return None
        return gui.course_lookup.get(selected_label)

    @staticmethod
    def build_semester_from_selection(
        gui: object,
        selected_label: str,
    ) -> Semester | None:
        """Resolve the selected Semester object from the GUI."""
        if selected_label in {"", "Select a Semester"}:
            return None

        selected_semester = gui.semester_lookup.get(selected_label)
        if selected_semester is not None:
            gui.current_semester = selected_semester
        return selected_semester

    @staticmethod
    def savefileas(
        filelist: tk.Listbox,
        gui: object,
        selected_course_label: str,
        selected_semester_label: str,
    ) -> None:
        """Handle the final save intent.

        CHANGE NOTE:
        This still does not perform full persistence for moved/saved files, but
        it now saves semester/course state back to a text file each time the
        user associates a course with a semester.
        """
        selected_course = Eventhandler.build_course_from_selection(
            gui, selected_course_label
        )
        selected_semester = Eventhandler.build_semester_from_selection(
            gui, selected_semester_label
        )

        if selected_course is None or selected_semester is None:
            return

        if selected_course not in selected_semester.courses:
            selected_semester.add_course(selected_course)
            Eventhandler.write_state_file(gui.save_file, gui.semesters)

        # CHANGE NOTE:
        # Save dialogs now open inside ./CMU/<year>/<semester>.
        directory = gui.cmu_root / str(selected_semester.year) / selected_semester.season

        for i in filelist.curselection():
            file = filelist.get(i)
            asksaveasfile(
                mode="w",
                confirmoverwrite=True,
                initialdir=str(directory),
                initialfile=file,
            )

    @staticmethod
    def prepfilestruct(semesters: list[Semester], cmu_root: Path) -> None:
        """Prepare folders from Semester objects under ./CMU.

        CHANGE NOTE:
        This creates only year/semester folders. Class folders are intentionally
        left for later manual or explicit logic.
        """
        for semester in semesters:
            sem_dir = cmu_root / str(semester.year) / semester.season
            try:
                sem_dir.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                print(f"Permission denied: Unable to create '{sem_dir}'.")

    @staticmethod
    def write_state_file(save_file: Path, semesters: list[Semester]) -> None:
        """Write a simple text save file.

        Format:
        - one SEMESTER line per semester
        - optional COURSE lines under that semester

        This is intentionally simple because the persistence design is still
        undecided.
        """
        save_file.parent.mkdir(parents=True, exist_ok=True)
        lines: list[str] = []

        for semester in semesters:
            lines.append(f"SEMESTER|{semester.year}|{semester.season}")
            for course in semester.courses:
                lines.append(
                    "COURSE|"
                    f"{semester.year}|{semester.season}|"
                    f"{course.dept.name}|{course.number}|{course.name}"
                )

        save_file.write_text("\n".join(lines), encoding="utf-8")

    @staticmethod
    def load_state_file(save_file: Path) -> list[Semester]:
        """Load Semester/Course state from the simple text save file."""
        if not save_file.exists():
            return []

        semesters: list[Semester] = []
        semester_lookup: dict[tuple[int, str], Semester] = {}
        tag_lookup: dict[str, Tag] = {}

        for raw_line in save_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split("|")
            record_type = parts[0]

            if record_type == "SEMESTER" and len(parts) == 3:
                year = int(parts[1])
                season = parts[2]
                semester = Semester(year=year, season=season)
                semesters.append(semester)
                semester_lookup[(year, season)] = semester

            elif record_type == "COURSE" and len(parts) == 6:
                year = int(parts[1])
                season = parts[2]
                dept_name = parts[3]
                course_number = int(parts[4])
                course_name = parts[5]

                semester = semester_lookup.get((year, season))
                if semester is None:
                    continue

                if dept_name not in tag_lookup:
                    tag_lookup[dept_name] = Eventhandler.make_tag(
                        dept_name,
                        f"{dept_name} loaded from save file",
                    )

                course = Course(course_name, course_number, tag_lookup[dept_name])
                if not Eventhandler.course_exists_in_semester(semester, course):
                    semester.add_course(course)

        return semesters

    @staticmethod
    def scan_semesters_from_fs(cmu_root: Path) -> list[Semester]:
        """Fallback only: rebuild Semester objects by scanning ./CMU."""
        semesters: list[Semester] = []
        for year_dir in sorted(cmu_root.iterdir()):
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue

            year = int(year_dir.name)
            for sem_dir in sorted(year_dir.iterdir()):
                if sem_dir.is_dir() and sem_dir.name in Eventhandler.SEASONS:
                    semesters.append(Semester(year=year, season=sem_dir.name))
        return semesters

    @staticmethod
    def course_exists_in_semester(semester: Semester, course: Course) -> bool:
        """Check course equality by field values, not object identity."""
        for existing in semester.courses:
            if (
                existing.name == course.name
                and existing.number == course.number
                and existing.dept.name == course.dept.name
            ):
                return True
        return False

    @staticmethod
    def make_tag(name: str, desc: str = "") -> Tag:
        """Small helper used by GUI setup for Tag creation."""
        tag = Tag()
        tag.set_name(name)
        tag.set_description(desc)
        return tag
