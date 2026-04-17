"""
    Course class for the file sorter
"""
from src.tags import Tag


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

        Args:
            name:   str - course title
            num:    int - course num
            dept:   Tag - course dept
        """
        self._name = name
        self._number = num
        self._dept = dept

    @property
    def name(self) -> str:
        """Getter
        """
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        """ Setter """
        if val == "":
            raise ValueError("Class: Course, must give a name.")
        self._name = val

    @property
    def number(self) -> int:
        """Getter
        """
        return self._number

    @number.setter
    def number(self, val: int) -> None:
        """ Setter """
        if val < 90 or val > 499:
            raise ValueError("Class: Course, number must be between 90 & 499.")
        self._number = val

    @property
    def dept(self) -> Tag:
        """Getter
        """
        return self._dept.name

    @dept.setter
    def dept(self, val: Tag) -> None:
        """ Setter """
        if len(val.name) != 4:
            raise ValueError("Class: Course, Tag.name must fit format of 'ABCD'.")
        self._dept = val

    def __str__(self) -> str:
        """ Returns a str representation of the class.
            Output is Dept Course Course-name

        Returns:
            str: str rep of Course
        """
        return f"{self._dept} {self._number} {self._name}"

