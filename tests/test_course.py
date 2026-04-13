"""
Unittesting Course class
"""


import unittest
import pytest
from hypothesis import given, strategies as st
from guiFiles.course import Course
from guiFiles.tags import Tag


class TestCourse(unittest.TestCase):
    """
    Unittesting Course class
    """
    valid_tag = st.text(
        #alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
        alphabet="QWERTYUIOPASDFGHJKLZXCVBNM",
        min_size=4,
        max_size=4
    )

    valid_course = st.text(
        alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
        min_size=1,
        max_size=25
    )

    valid_num = st.integers(
        min_value=90,
        max_value=499
    )

    def setUp(self) -> None:
        """ Sets up a Course to do specific tests """
        t = Tag()
        t.set_name("CSCI")
        self.c = Course("Computer Science 1", 110, t)

    @given(valid_tag, valid_course, valid_num)
    def test_Course_constructor(self, dept: str, name: str, num: int) -> None:
        """ Test the constructor of Course """
        t = Tag()
        t.set_name(dept)

        c = Course(name, num, t)

        assert c.dept == dept
        assert c.name == name
        assert c.number == num

    @given(valid_tag, valid_course, valid_num)
    def test_str(self, dept: str, name: str, num: int) -> None:
        """Tests the overload for __str__ using hypothesis."""
        t = Tag()
        t.set_name(dept)

        c = Course(name, num, t)

        expected = f"{dept} {int(num)} {name}"
        self.assertEqual(str(c), expected)

    def test_getter_name(self) -> None:
        """Tests getter method for name"""
        self.assertEqual(self.c.name, "Computer Science 1")

    @given(valid_course)
    def test_setter_name(self, name: str) -> None:
        """Tests setter method for name using hypothesis."""
        self.c.name = name
        assert self.c.name == name

    def test_getter_num(self) -> None:
        """Tests getter method for name"""
        self.assertEqual(self.c.number, 110)

    @given(valid_num)
    def test_setter_num(self, num: int) -> None:
        """Tests setter method for name using hypothesis."""
        self.c.number = num
        assert self.c.number == num

    def test_getter_dept(self) -> None:
        """Tests getter method for name"""
        self.assertEqual(self.c.dept, "CSCI")

    @given(valid_course)
    def test_setter_dept(self, dept: str) -> None:
        """Tests setter method for name using hypothesis."""
        self.c._dept.set_name(dept)
        assert str(self.c._dept) == dept

