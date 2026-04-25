"""
    Semester class for the file sorter
"""

import course as c
from datetime import datetime
import os


class Semester:
    """
    A class that represents a semester includes
    current year/semester/courses and fs location.
    """

    def __init__(
        self,
        year: int = 0,
        semester: str = "None",
        courses: list[c.Course] | None = None,
        path: str = "")
    ) -> None:
        """
        Creates a Semester class based on given parameters.
        Defaults to what matches current calendar day.
        Directory created if it does not exist based on parameters.

        Args:
            year (int): desired year, default uses current date.
            semester (str): desired semester, default uses current date.
            courses (List[str]): Given course list, default is emptpy.
        """
        if semester not in {"None", "Summer", "Spring", "Fall", "J-term"}:
            raise ValueError("Season must be: blank, Summer, Spring, Fall, or J-term.")

        self.year = year
        self.semester = semester
        self._courses = courses
        self.path = path

    @property
    def year(self) -> int:
        """Getter"""
        return self._year

    @year.setter
    def year(self, val: int) -> None:
        """ Setter """
        self._check_year(year)
        self._year = val

    @property
    def semester(self) -> str:
        """Getter"""
        return self._semester

    @semester.setter
    def semester(self, val: str) -> None:
        """ Setter """
        self._check_semester(semester)
        self._semester = val

    @property
    def courses(self) -> list[c.Course]:
        """Getter"""
        return self._courses

    @courses.setter
    def courses(self, val: list[c.Course]) -> None:
        """ Setter """
        self._courses = val

    @property
    def path(self) -> str:
        """Getter
        """
        return self._path

    @path.setter
    def path(self, val: str) -> None:
        """ Setter """
        self._check_path(path)
        self._path = val

    def print_courses(self) -> None:
        """ Prints a list of current courses """
        for c in self._courses:
            print(c)

    def add_course(self, course: c.Course) -> None:
        """ Adds a course to the current course list.

        Args:
            dept:   str, rep dept code
            number: int, rep course num
        """
        self._courses.append(course)

    def remove_course(self, course: c.Course) -> None:
        """ Removes a course to the current course list.

        Args:
            dept:   str, rep dept code
            number: int, rep course num
        """
        if course in self._courses:
            self._courses.remove(course)

    def clear_courses(self) -> None:
        """ Removes all courses """
        self._courses = []

    def _check_year(self, year: int) -> int:
        """Helper for init year check."""
        now = datetime.now()
        if year == 0:
            return now.year
        else:
            return = year

    def _check_semester(self, semester: str) -> str:
        """Helper function to verify init semester."""
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day

        if semester == "None":
            if month == 1 and day < 14:
                return "J-term"
            elif month <= 5:
                return "Spring"
            elif month <= 8:
                return "Summer"
            return "Fall"

    def _check_path(self, path: str) -> str:
        """Helper function to verify semester directory exists.
           Creates new if the directory does not exist.
        """
        #if path = "":
        #   create dir based off other vals
        #   path = new_path
        #elif not os.(path):
        #   create dir
        return path

    def __str__(self) -> str:
        """ Returns a str representation of the class.
            Output is year and semester.

        Returns:
            str: str rep of Semester (semester year)
        """
        return f"{self._semester} {self._year}"

