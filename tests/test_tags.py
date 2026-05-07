"""
Unittesting Tag class
"""


import unittest
from hypothesis import given, strategies as st
from src.tags import Tag


class TestTag(unittest.TestCase):
    """
    Unittesting Tag class
    """
    valid_input = st.text(
        alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
    )

    def setUp(self) -> None:
        """Sets up a Tag to do tests."""
        self.t1 = Tag()

    @given(valid_input)
    def test_setter_desc(self, desc: str) -> None:
        """Tests setter method for name using hypothesis."""
        self.t1.set_description(desc)
        assert self.t1.desc == desc
