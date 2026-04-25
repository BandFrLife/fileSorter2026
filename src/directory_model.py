"""
Class module for DirectoryModel
    Controls the fs access
"""

import os
import datetime

class DirectoryModel:
    """
    """
    def __init__(self, base_dir: str = "CMU"):
        """Initializes class.

        Args:
            base_dir (str): highest directory of prgm, defaults to CMU.

        Returns:
            None
        """
        self.base_dir = base_dir

    def get_dirs(self, path: str) -> list[str]:
        """Obtain all directories from given path.

        Args:
            path (str): path to directory.
.
        Returns:
            list[str]: list of all directories found, otherwise empty list
        """
        try:
            items = os.listdir(path)
        except FileNotFoundError:
            return []

        dirs = []
        for name in items:
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path):
                dirs.append(name)

        dirs.sort()
        return dirs

    def get_items(self, path: str) -> list[str]:
        """Obtain all files/dirs from given directory.

        Args:
            path (str): path to directory.
.
        Returns:
            list[str]: list of all directories/files found, otherwise empty list
        """
        try:
            items = os.listdir(path)
        except FileNotFoundError:
            return []

        items.sort()
        return items

    def get_current_year(self) -> str:
        """Get the current year.

        Returns:
            str: The current year as a string.
        """
        return str(datetime.datetime.now().year)

    def get_current_semester(self) -> str:
        """Get the current semester based on date.

        Returns:
            str: Current semester (J-term, Spring, Summer, Fall).
        """
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day

        if month == 1 and day < 14:
            return "J-term"
        elif month <= 5:
            return "Spring"
        elif month <= 8:
            return "Summer"
        return "Fall"

