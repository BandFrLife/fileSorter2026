"""
    Course class for the file sorter
"""
#class Tag:
#    def __init__(self) -> None:
#        self.dept = "CSCI"
#
#    def __str__(self) -> str:
#        return f"{self.dept}"

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
        self._name = val

    @property
    def number(self) -> int:
        """Getter
        """
        return self._number

    @number.setter
    def number(self, val: int) -> None:
        """ Setter """
        self._number = val

    @property
    def dept(self) -> Tag:
        """Getter
        """
        return self._dept

    @dept.setter
    def dept(self, val: Tag) -> None:
        """ Setter """
        self._dept = val

    def __str__(self) -> str:
        """ Returns a str representation of the class.
            Output is Dept Course Course-name

        Returns:
            str: str rep of Course
        """
        return f"{self._dept} {self._number} {self._name}"

