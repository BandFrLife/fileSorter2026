"""main program file
"""
import tkinter as tk
from guiEvents import eventHandler


window = tk.Tk()
window.title("File Sorter v0.1")
window.geometry('1080x550+75+75')  # window size, offset from monitor size
frame = tk.Frame()

pathEntry = tk.Entry(window,
                     textvariable=tk.StringVar(value="input Directory here"),
                     width=50
                     )
pathEntry.grid(row=2, column=1, padx=5, pady=7)

pathPick = tk.Button(window,
                     text="Pick Directory",
                     anchor="ne",
                     padx=15,  # size of button in x
                     pady=3  # size of button in y
                     )
pathPick.bind('<Button-1>', lambda event: eventHandler.pickPath((), pathEntry))
pathPick.grid(row=2, column=2, padx=5, pady=7)

fileEntry = tk.Entry(window,
                     textvariable=tk.StringVar(value="input File here"),
                     width=50
                     )
fileEntry.grid(row=3, column=1, padx=5, pady=7)

filePick = tk.Button(window,
                     text="Pick File",
                     anchor="se",
                     padx=20,  # size of button in x
                     pady=3  # size of button in y
                     )
filePick.bind('<Button-1>', lambda event: eventHandler.pickFile((), fileEntry))
filePick.grid(row=3, column=2, padx=5, pady=7)

window.mainloop()
