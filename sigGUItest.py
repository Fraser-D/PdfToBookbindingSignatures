import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def open_file(*args):
    # temp = fd.askopenfilename(
    #     title="Select a PDF file", filetypes=[("pdf files", ".PDF")]
    # )
    # pdf_path.set(temp.)
    print(pdf_path)


root = tk.Tk()
root.title("Reorder PDF into Bookbinding Signatures for Duplex Printing")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=('N', "W", "S", 'E'))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

title1 = ttk.Label(mainframe, text="Pdf to Bookbinding Signatures")
title1.grid(column=0, row=0, sticky='W')
title2 = ttk.Label(
    mainframe, text="A simple program for reordering the pages of a PDF file into bookbinding signatures for duplex printing")
title2.grid(column=0, row=2)

chooselab = ttk.Label(mainframe, text="Choose a PDF file to work on")
chooselab.grid(column=0, row=4, sticky="W")
pdf_path = tk.StringVar()
inputfile = ttk.Button(mainframe, text="Choose file",
                       command=lambda: open_file())
inputfile.grid(column=0, row=6, sticky="W")


exitbutton = ttk.Button(mainframe, text="EXIT/cancel", command=root.quit)
exitbutton.grid(row=20, column=0, sticky="W")
# # exitprog = 1
# file_entry = ttk.Entry(mainframe, width=10)
# file_entry.grid(mainframe)
# ttk.Button(mainframe, text="Run The Program").grid()
# ttk.Button(mainframe, text="Cancel/close", command='exitprog').grid()

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
# file_entry.focus()

root.mainloop()
print(pdf_path)
