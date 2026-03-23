"""main program file
"""
import tkinter as tk
from tkinter import ttk as tkk
from guievents import Eventhandler

tagOptions = ["Math", "English", "Science", "ComputerScience"]
window = tk.Tk()
window.title("File Sorter v0.1")
window.geometry('700x200+75+75')  # window size(x,y), offset from monitor size
#frame = tk.Frame()
for row in range(6):
    window.rowconfigure(row, weight=2)
for col in range(6):
    window.columnconfigure(col, weight=2)
window.rowconfigure(0, weight=1)

pathEntry = tk.Entry(window,
                     textvariable=tk.StringVar(value="input Directory here"),
                     width=50
                     )
pathEntry.grid(row=1, column=0, padx=5, pady=7, sticky="w")

pathPick = tk.Button(window,
                     text="Pick Directory",
                     anchor="ne",
                     padx=15,  # size of button in x
                     pady=3  # size of button in y
                     )
pathPick.bind('<Button-1>', lambda event: Eventhandler.pickpath((), pathEntry))
pathPick.grid(row=1, column=1, padx=5, pady=7, sticky="w")

fileEntry = tk.Entry(window,
                     textvariable=tk.StringVar(value="input File here"),
                     width=50
                     )
fileEntry.grid(row=2, column=0, padx=5, pady=7, sticky="w")

filePick = tk.Button(window,
                     text="Pick File",
                     anchor="se",
                     padx=20,  # size of button in x
                     pady=3  # size of button in y
                     )
filePick.bind('<Button-1>', lambda event: Eventhandler.pickfile((), fileEntry))
filePick.grid(row=2, column=1, padx=5, pady=7, sticky="w")

tagDropdown = tkk.Combobox(window,
                           values=tagOptions,
                           state="readonly",
                           width=20
                           )
tagDropdown.set("Select a Subject")
tagDropdown.grid(row=3, column=0, padx=5, pady=7, sticky="w")

submit = tk.Button(window,
                   text="Save file",
                   anchor="se",
                   padx=20,  # size of button in x
                   pady=3  # size of button in y
                   )
submit.bind('<Button-1>', lambda event: Eventhandler.savefileas((),
                                                                fileEntry,
                                                                pathEntry,
                                                                tagDropdown))
submit.grid(row=6, column=6, padx=5, pady=7, sticky="se")

window.mainloop()

# add a list of dropdown menu for tags to be put onto file
# add constraints to what can be input into entry/ add error catching for
#                                                        invalid entries
