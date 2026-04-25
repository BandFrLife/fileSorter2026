"""
    Semester class for the file sorter
"""

# CHANGE NOTE:
# Fixed Course import and always initialize the course list so GUI code can
# safely create Semester objects before any courses are attached.
import course_updated as c
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
        if season not in {"None", "Summer", "Spring", "Fall", "J-term"}:
            raise ValueError(
                "Season must be: blank, Summer, Spring, Fall, or J-term."
            )

        now = datetime.now()
        self._year = now.year if year == 0 else year

        if season == "None":
            if now.month <= 1:
                self._season = "J-term"
            elif now.month <= 5:
                self._season = "Spring"
            elif now.month <= 8:
                self._season = "Summer"
            else:
                self._season = "Fall"
        else:
            self._season = season

        self._courses = list(courses) if courses is not None else []

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, val: int) -> None:
        self._year = val

    @property
    def season(self) -> str:
        return self._season

    @season.setter
    def season(self, val: str) -> None:
        self._season = val

    @property
    def courses(self) -> list[c.Course]:
        return self._courses

    @courses.setter
    def courses(self, val: list[c.Course]) -> None:
        self._courses = val

    def print_courses(self) -> None:
        for course in self._courses:
            print(course)

    def add_course(self, course: c.Course) -> None:
        self._courses.append(course)

    def remove_course(self, course: c.Course) -> None:
        if course in self._courses:
            self._courses.remove(course)

    def clear_courses(self) -> None:
        self._courses = []

    def __str__(self) -> str:
        return f"{self._season} {self._year}"
