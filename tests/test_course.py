"""
Unittesting Course class
"""


import unittest
from hypothesis import given, strategies as st
from src.course import Course
from src.tags import Tag


class TestCourse(unittest.TestCase):
    """
    Unittesting Course class
    """
    valid_tag = st.text(
        # alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
        alphabet="QWERTYUIOPASDFGHJKLZXCVBNM",
        min_size=4,
        max_size=4
    )

    invalid_tag = st.one_of(
        st.text(
            alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
            min_size=5
        ),
        st.text(
            alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
            max_size=3
        )
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

    invalid_num = st.one_of(
        st.integers(min_value=500),
        st.integers(max_value=89)
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

        assert str(c.dept) == dept
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

        t = Tag()
        with self.assertRaises(ValueError):
            Course("", 2026, t)

    def test_getter_num(self) -> None:
        """Tests getter method for name"""
        self.assertEqual(self.c.number, 110)

    @given(valid_num, invalid_num)
    def test_setter_num(self, num: int, invalid: int) -> None:
        """Tests setter method for name using hypothesis."""
        self.c.number = num
        assert self.c.number == num

        with self.assertRaises(ValueError):
            self.c.number = invalid

    def test_getter_dept(self) -> None:
        """Tests getter method for name"""
        tag = Tag()
        tag.set_name("CSCI")
        self.assertEqual(str(self.c.dept), tag.name)

    @given(valid_course)
    def test_setter_dept(self, dept: str) -> None:
        """Tests setter method for name using hypothesis."""
        self.c._dept.set_name(dept)
        assert str(self.c._dept) == dept

    @given(invalid_tag)
    def test_setter_dept_invalid(self, dept: str) -> None:
        """Tests setter method ValueError for name using hypothesis."""
        t = Tag()
        t.set_name(dept)

        with self.assertRaises(ValueError):
            self.c.dept = t
