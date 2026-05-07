"""Event functions for the file sorter GUI."""

from __future__ import annotations

import shutil
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo


class Eventhandler:
    """Holds the actions called by the GUI buttons."""

    def __init__(self) -> None:
        self.source_dir: Path | None = None
        self.project_root = Path(__file__).resolve().parent
        self.current_year = "2026"

    def prepfilestruct(self) -> None:
        """Create the basic 2026 semester folders if missing."""
        for semester in ["Fall", "J-term", "Spring", "Summer"]:
            (self.project_root / self.current_year / semester).mkdir(
                parents=True,
                exist_ok=True,
            )

    def populatelist(self, box: tk.Listbox) -> None:
        """Open a directory and list only files in the file listbox."""
        picked_dir = askdirectory()
        if not picked_dir:
            return

        self.source_dir = Path(picked_dir)
        box.delete(0, tk.END)

        for item in sorted(self.source_dir.iterdir()):
            if item.is_file():
                box.insert(tk.END, item.name)

    def add_tag(self, tag_entry: tk.Entry, tag_box: tk.Listbox) -> None:
        """Add one manually typed tag to the tag listbox."""
        new_tag = tag_entry.get().strip()
        if not new_tag:
            showerror("Missing tag", "Enter a tag name first.")
            return

        current_tags = tag_box.get(0, tk.END)
        if new_tag not in current_tags:
            tag_box.insert(tk.END, new_tag)

        tag_entry.delete(0, tk.END)

    def savefileas(
        self,
        filelist: tk.Listbox,
        semester: str,
        course_name: str,
        tag_box: tk.Listbox,
    ) -> None:
        """Copy the selected file into 2026/semester/course_name."""
        if self.source_dir is None:
            showerror("No directory", "Pick a directory first.")
            return

        selected_tag_indexes: tuple[int, ...] = (
            tag_box.curselection()  # type: ignore[no-untyped-call]
        )
        if semester not in {"Fall", "J-term", "Spring", "Summer"}:
            showerror("Missing semester", "Select a semester.")
            return

        course_name = course_name.strip()
        if not course_name:
            showerror("Missing class", "Enter the class/course name.")
            return

        for i in filelist.curselection():  # type: ignore[no-untyped-call]
            filename = (filelist.get(i))
            source_path = self.source_dir / filename
            destination_dir = (
                self.project_root
                / self.current_year
                / semester
                / course_name
            )
            destination_dir.mkdir(parents=True, exist_ok=True)

            destination_path = destination_dir / filename
            shutil.copy2(source_path, destination_path)

            selected_tags = [tag_box.get(i) for i in selected_tag_indexes]

            required_tags = [self.current_year, semester, course_name]
            all_tags = []
            for tag in required_tags + selected_tags:
                if tag not in all_tags:
                    all_tags.append(tag)

            tag_file = destination_path.with_suffix(
                destination_path.suffix + ".tags.txt")
            tag_file.write_text("\n".join(all_tags) + "\n", encoding="utf-8")

            showinfo("Saved", f"Saved to:\n{destination_path}")
