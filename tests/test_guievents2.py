"""
Unittesting Eventhandler class

Provided by ChatGPT
Too much to do but want full coverage.
"""

import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import patch

from hypothesis import given, strategies as st

from src.guievents2 import Eventhandler


class FakeEntry:
    """Fake Entry widget for testing."""

    def __init__(self, value: str = "") -> None:
        self.value = value
        self.deleted = False

    def get(self) -> str:
        """Return entry value."""
        return self.value

    def delete(self, start: object, end: object) -> None:
        """Fake delete method."""
        self.value = ""
        self.deleted = True


class FakeListbox:
    """Fake Listbox widget for testing."""

    def __init__(self) -> None:
        self.items: list[str] = []
        self.selected: tuple[int, ...] = ()
        self.deleted = False

    def curselection(self) -> tuple[int, ...]:
        """Return selected indexes."""
        return self.selected

    def get(self, *args: object) -> str | tuple[str, ...]:
        """Return one item or all items."""
        if len(args) == 2:
            return tuple(self.items)

        index_obj = args[0]

        if not isinstance(index_obj, int):
            raise TypeError(
                "FakeListbox index must be int")  # pragma: no cover

        return self.items[index_obj]

    def insert(self, index: object, value: str) -> None:
        """Insert item into fake listbox."""
        self.items.append(value)

    def delete(self, start: object, end: object) -> None:
        """Delete all items from fake listbox."""
        self.items.clear()
        self.deleted = True


class TestEventhandler(unittest.TestCase):
    """
    Unittesting Eventhandler class
    """

    valid_tag = st.text(
        alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
        min_size=1,
        max_size=25
    )

    valid_course = st.text(
        alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",
        min_size=1,
        max_size=25
    )

    valid_semester = st.sampled_from(
        ["Fall", "J-term", "Spring", "Summer"]
    )

    invalid_semester = st.text(
        alphabet="qwertyuiopasdfghjklzxcvbnm",
        min_size=1,
        max_size=20
    ).filter(lambda x: x not in {"Fall", "J-term", "Spring", "Summer"})

    def setUp(self) -> None:
        """ Sets up an Eventhandler to do specific tests """
        self.e = Eventhandler()

    def test_Eventhandler_constructor(self) -> None:
        """ Test the constructor of Eventhandler """
        self.assertIsNone(self.e.source_dir)
        self.assertEqual(self.e.current_year, "2026")
        self.assertIsInstance(self.e.project_root, Path)

    def test_prepfilestruct(self) -> None:
        """Tests prepfilestruct creates semester directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            self.e.project_root = Path(temp_dir)
            self.e.prepfilestruct()

            for semester in ["Fall", "J-term", "Spring", "Summer"]:
                path = self.e.project_root / "2026" / semester
                self.assertTrue(path.exists())
                self.assertTrue(path.is_dir())

    def test_populatelist_no_directory(self) -> None:
        """Tests populatelist returns if no directory is picked."""
        box = FakeListbox()

        with patch("src.guievents2.askdirectory", lambda: ""):
            self.e.populatelist(cast(tk.Listbox, box))

        self.assertIsNone(self.e.source_dir)
        self.assertFalse(box.deleted)
        self.assertEqual(box.items, [])

    def test_populatelist(self) -> None:
        """Tests populatelist inserts only files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            file_path = temp_path / "notes.txt"
            dir_path = temp_path / "folder"

            file_path.write_text("test", encoding="utf-8")
            dir_path.mkdir()

            box = FakeListbox()

            with patch("src.guievents2.askdirectory", lambda: temp_dir):
                self.e.populatelist(cast(tk.Listbox, box))

            self.assertEqual(self.e.source_dir, temp_path)
            self.assertTrue(box.deleted)
            self.assertEqual(box.items, ["notes.txt"])

    @given(valid_tag)
    def test_add_tag(self, tag: str) -> None:
        """Tests add_tag using hypothesis."""
        tag_entry = FakeEntry(tag)
        tag_box = FakeListbox()

        self.e.add_tag(
            cast(tk.Entry, tag_entry),
            cast(tk.Listbox, tag_box),
        )

        self.assertEqual(tag_box.items, [tag])
        self.assertTrue(tag_entry.deleted)

    @given(valid_tag)
    def test_add_tag_duplicate(self, tag: str) -> None:
        """Tests add_tag does not add duplicate tags."""
        tag_entry = FakeEntry(tag)
        tag_box = FakeListbox()
        tag_box.items = [tag]

        self.e.add_tag(
            cast(tk.Entry, tag_entry),
            cast(tk.Listbox, tag_box),
        )

        self.assertEqual(tag_box.items, [tag])
        self.assertTrue(tag_entry.deleted)

    def test_add_tag_empty(self) -> None:
        """Tests add_tag shows error for empty tag."""
        calls: list[tuple[str, str]] = []

        def fake_showerror(title: str, message: str) -> None:
            calls.append((title, message))

        tag_entry = FakeEntry("   ")
        tag_box = FakeListbox()

        with patch("src.guievents2.showerror", fake_showerror):
            self.e.add_tag(
                cast(tk.Entry, tag_entry),
                cast(tk.Listbox, tag_box),
            )

        self.assertEqual(len(calls), 1)
        self.assertEqual(tag_box.items, [])
        self.assertFalse(tag_entry.deleted)

    def test_savefileas_no_source_dir(self) -> None:
        """Tests savefileas shows error when no source directory exists."""
        calls: list[tuple[str, str]] = []

        def fake_showerror(title: str, message: str) -> None:
            calls.append((title, message))

        filelist = FakeListbox()
        tag_box = FakeListbox()

        with patch("src.guievents2.showerror", fake_showerror):
            self.e.savefileas(
                cast(tk.Listbox, filelist),
                "Fall",
                "CSCI110",
                cast(tk.Listbox, tag_box),
            )

        self.assertEqual(len(calls), 1)

    @given(invalid_semester, valid_course)
    def test_savefileas_invalid_semester(
        self,
        semester: str,
        course: str
    ) -> None:
        """Tests savefileas shows error for invalid semester."""
        calls: list[tuple[str, str]] = []

        def fake_showerror(title: str, message: str) -> None:
            calls.append((title, message))

        filelist = FakeListbox()
        tag_box = FakeListbox()

        self.e.source_dir = Path("fake_dir")

        with patch("src.guievents2.showerror", fake_showerror):
            self.e.savefileas(
                cast(tk.Listbox, filelist),
                semester,
                course,
                cast(tk.Listbox, tag_box),
            )

        self.assertEqual(len(calls), 1)

    @given(valid_semester)
    def test_savefileas_empty_course(self, semester: str) -> None:
        """Tests savefileas shows error for empty course."""
        calls: list[tuple[str, str]] = []

        def fake_showerror(title: str, message: str) -> None:
            calls.append((title, message))

        filelist = FakeListbox()
        tag_box = FakeListbox()

        self.e.source_dir = Path("fake_dir")

        with patch("src.guievents2.showerror", fake_showerror):
            self.e.savefileas(
                cast(tk.Listbox, filelist),
                semester,
                "   ",
                cast(tk.Listbox, tag_box),
            )

        self.assertEqual(len(calls), 1)

    @given(valid_semester, valid_course)
    def test_savefileas(self, semester: str, course: str) -> None:
        """Tests savefileas copies file and creates tag file."""
        calls: list[tuple[str, str]] = []

        def fake_showinfo(title: str, message: str) -> None:
            calls.append((title, message))

        with tempfile.TemporaryDirectory() as source_temp:
            with tempfile.TemporaryDirectory() as project_temp:
                source_path = Path(source_temp)
                project_path = Path(project_temp)

                test_file = source_path / "notes.txt"
                test_file.write_text("hello", encoding="utf-8")

                self.e.source_dir = source_path
                self.e.project_root = project_path

                filelist = FakeListbox()
                filelist.items = ["notes.txt"]
                filelist.selected = (0,)

                tag_box = FakeListbox()
                tag_box.items = ["Homework"]
                tag_box.selected = (0,)

                with patch("src.guievents2.showinfo", fake_showinfo):
                    self.e.savefileas(
                        cast(tk.Listbox, filelist),
                        semester,
                        course,
                        cast(tk.Listbox, tag_box),
                    )

                destination = (
                    project_path
                    / "2026"
                    / semester
                    / course
                    / "notes.txt"
                )

                tag_file = destination.with_suffix(".txt.tags.txt")

                self.assertTrue(destination.exists())
                self.assertTrue(tag_file.exists())

                tags = tag_file.read_text(encoding="utf-8")

                self.assertIn("2026", tags)
                self.assertIn(semester, tags)
                self.assertIn(course, tags)
                self.assertIn("Homework", tags)

                self.assertEqual(len(calls), 1)
