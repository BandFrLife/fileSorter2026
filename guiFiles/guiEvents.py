"""Seperate file that holds all events and calls from the gui

Returns:
    None: Nada, Nothing
"""
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter as tk


class eventHandler ():

    def pickFile(self, entry: tk.Entry) -> str:
        entry.delete(0, tk.END)
        entry.insert(0, askopenfilename())
    
    def pickPath(self, entry: tk.Entry) -> str:
        entry.delete(0, tk.END)
        entry.insert(0, askdirectory())
