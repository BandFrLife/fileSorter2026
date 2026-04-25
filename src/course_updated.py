"""
    Course class for the file sorter
"""
# CHANGE NOTE:
# Fixed the Tag import so GUI / event code can actually use Course.
from tags import Tag


class Course:
    """
    A class that represents a course that includes
    department, course number, course name
    """
    def __init__(
        self,
        name: str,
        num: int,
        dept: Tag
    ) -> None:
        """
        Populates a class based on the course
        name and number, and the department.
        """
        self.name = name
        self.number = num
        self.dept = dept

    @property
    def name(self) -> str:
        """Getter"""
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        """Setter"""
        if val == "":
            raise ValueError("Class: Course, must give a name.")
        self._name = val

    @property
    def number(self) -> int:
        """Getter"""
        return self._number

    @number.setter
    def number(self, val: int) -> None:
        """Setter"""
        if val < 90 or val > 499:
            raise ValueError("Class: Course, number must be between 90 & 499.")
        self._number = val

    @property
    def dept(self) -> Tag:
        """Getter"""
        return self._dept

    @dept.setter
    def dept(self, val: Tag) -> None:
        """Setter"""
        if len(val.name) != 4:
            raise ValueError("Class: Course, Tag.name must fit format of 'ABCD'.")
        self._dept = val

    def __str__(self) -> str:
        """Returns a str representation of the class."""
        return f"{self._dept} {self._number} {self._name}"
