"""
    Semester class for the file sorter
"""

import course as c
from datetime import datetime


class Semester:
    """
    A class that represents a semester includes
    current year/season/courses.
    """

    def __init__(
        self,
        year: int = 0,
        season: str = "None",
        courses: list[c.Course] | None = None
    ) -> None:
        """
        Creates a Semester based on current calendar year.
        Sets the year and season based on input or creation
        date.

        Args:
            year:
            season:
            courses:
        """
        if season not in {"None", "Summer", "Winter", "Fall", "J-term"}:
            raise ValueError("Season must be: blank, Summer, Spring, Fall, or J-term.")

        now = datetime.now()

        if year == 0:
            self._year = now.year
        else:
            self._year = year

        if season == "None":
            if now.month < 6:
                self._season = "Fall"
            elif now.month < 8:
                self._season = "Summer"
            else:
                self._season = "Winter"
        else:
            self._season = season

        if courses:
            self._courses = courses

    @property
    def year(self) -> int:
        """Getter
        """
        return self._year

    @year.setter
    def year(self, val: int) -> None:
        """ Setter """
        self._year = val

    @property
    def season(self) -> str:
        """Getter
        """
        return self._season

    @season.setter
    def season(self, val: str) -> None:
        """ Setter """
        self._season = val

    @property
    def courses(self) -> list[c.Course]:
        """Getter
        """
        return self._courses

    @courses.setter
    def courses(self, val: list[c.Course]) -> None:
        """ Setter """
        self._courses = val

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

    def __str__(self) -> str:
        """ Returns a str representation of the class.
            Output is year and season.

        Returns:
            str: str rep of Semester (season year)
        """
        return f"{self._season} {self._year}"

