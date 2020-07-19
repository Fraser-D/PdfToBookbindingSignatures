# now building the whole thing into the gui

# ? possibly making an intermediate pdf with the blank pages?

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PyPDF2 import PdfFileReader as Pdfread
from PyPDF2 import PdfFileWriter as Pdfwrite
from PyPDF2 import PdfFileMerger as Pdfmerge
import os
import math


# ! I have no idea what these args are, or where they came from :)

# this had args a,b,c don't know why
def update_vars(var, indx, mode):
    sigpages = (sig_thickness.get() * 4)
    sig_thickness_x4.set(sigpages)
    newtotal.set(blank_start.get() + num_of_pages.get())
    sig_count.set(newtotal.get() // sigpages)
    leftoverpages = newtotal.get() % sigpages
    sig_remain.set(leftoverpages)

    if leftoverpages == 0:
        addblankends = 0,
    elif sig_count == 0:
        addblankends = (sigpages - newtotal)
    elif equal_ends_sig.get() == 1:
        addblankends = sigpages - leftoverpages
    else:
        addblankends = math.ceil(leftoverpages / 4) * 4 - leftoverpages

    end_blank_pages.set(addblankends)


def open_file():
    pdf_path.set(filedialog.askopenfilename(
        title="Select a PDF file", filetypes=[("pdf files", ".PDF")]
    ))
    pdf = Pdfread(pdf_path.get())
    num_of_pages.set(pdf.getNumPages())


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def shuffle(l, n):
    s = []
    n = n * 2
    s.append(l[(-1 - n)])
    s.append(l[(0 + n)])
    s.append(l[(1 + n)])
    s.append(l[(-2 - n)])
    return s


def signature_shuffle(pagelist):
    out = []
    for i in range(len(pagelist)//4):
        out.extend(shuffle(pagelist, i))
    return out


def shufoutput(arrayofarrays):
    shuf = []
    for line in arrayofarrays:
        shuf.append(signature_shuffle(line))
    flat = []
    for x in shuf:
        flat.extend(x)
    return flat

# pdf_path, pdf_output_path, blank_start replace with thses .get()
# pdftoproc, pdfdestination, startblanks   removed these


def process_the_pdf():

    confirm = tk.messagebox.askyesno(
        "Doing the thing", "Are you sure you want to do the thing?")
    if confirm == True:
        try:
            pdf = Pdfread(pdf_path.get())
            wf = Pdfwrite()
            wf.appendPagesFromReader(pdf)

            for i in range(blank_start.get()):
                wf.insertBlankPage(0)
            for i in range(int(end_blank_pages.get())):
                wf.addBlankPage()

            # ! --> here's where the shuffle goes, pos save temp pdf here?

            list_pages = []

            for i in range(wf.getNumPages()):
                list_pages.append(i)

            list_sigs_pages = []
            for group in chunker(list_pages, sig_thickness_x4.get()):
                list_sigs_pages.append(group)

            newpageorder = shufoutput(list_sigs_pages)

            newpdf = Pdfwrite()

            for page in newpageorder:
                newpdf.addPage(wf.getPage(page))

            up2 = Pdfwrite()
            up2 = turninto2up(newpdf)

            with open(pdf_output_path.get(), 'wb') as out:
                up2.write(out)

            tk.messagebox.showinfo(
                "Finished", "Finished, and maybe it even worked this time!")

        except FileNotFoundError:
            tk.messagebox.showerror(
                "File not found", "Either the input file or the output files is wrong.\nOr both of them. Who knows?")
            pass
    else:
        pass


# 2up based on code from https://github.com/mstamy2/PyPDF2/blob/master/Scripts/2-up.py
def turninto2up(pdfwr):
    temp = Pdfwrite()

    firstpagesize = pdfwr.getPage(0)
    offset = firstpagesize.mediaBox.getUpperRight_x()

    for iter in range(0, pdfwr.getNumPages()-1, 2):
        lhs = pdfwr.getPage(iter)
        rhs = pdfwr.getPage(iter+1)
        # ! this is the problem -->
        lhs.mergeTranslatedPage(rhs, offset, 0, True)
        temp.addPage(lhs)

    return temp


def output_file():
    pdf_output_path.set(filedialog.asksaveasfilename(
        title="Select a PDF file", filetypes=[("pdf files", ".PDF")], defaultextension=".pdf"
    ))


# GUI
root = tk.Tk()
root.title("Reorder PDF into Bookbinding Signatures for Duplex Printing")
mainf = ttk.Frame(root, padding="3 3 12 12")
mainf.grid(column=0, row=0, sticky=('N', "W", "S", 'E'))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

pdf_path = tk.Variable(root)
pdf_path.trace_add("write", update_vars)
sig_thickness = tk.IntVar(root, value=1)
sig_thickness.trace_add("write", update_vars)
blank_start = tk.IntVar(root, value=0)
blank_start.trace_add("write", update_vars)
equal_ends_sig = tk.BooleanVar(root, value=True)
equal_ends_sig.trace_add("write", update_vars)
pdf_output_path = tk.Variable(root)

sig_thickness_x4 = tk.IntVar(root, value=4)

num_of_pages = tk.IntVar(root, value=0)
num_of_pages.trace_add("write", update_vars)

sig_count = tk.IntVar(root, value=0)
sig_count.trace_add("write", update_vars)
sig_remain = tk.IntVar(root, value=0)
sig_remain.trace_add("write", update_vars)
newtotal = tk.IntVar(root, value=0)
newtotal.trace_add("write", update_vars)

end_blank_pages = tk.IntVar(root, value=0)
# end_blank_pages.trace_add("write", update_vars)


# Get pdf file

title1 = ttk.Label(mainf, text="Pdf to Bookbinding Signatures")
title1.grid(column=0, row=0, sticky='W')
title2 = ttk.Label(
    mainf, text="A simple program for reordering the pages of a PDF file into bookbinding signatures for duplex printing")
title2.grid(column=0, row=2, sticky="w", columnspan=4)

# # ? choose a pdf to edit
choose_label = ttk.Label(mainf, text="Choose a PDF file to work on")
choose_label.grid(column=0, row=4, sticky="W")
input_file = ttk.Button(mainf, text="Choose file",
                        command=lambda: open_file())
input_file.grid(column=0, row=6, sticky="W")

pdf_lable = ttk.Label(mainf, textvariable=pdf_path)
pdf_lable.grid(column=0, row=7, sticky="W")

in_count_lable = ttk.Label(mainf, text="this file has").grid(
    row=7, column=1, sticky='e')
in_count_lable2 = ttk.Label(mainf, text="pages").grid(
    row=7, column=3, sticky='w')
pdf_in_pagecount = ttk.Label(
    mainf, textvariable=num_of_pages)
pdf_in_pagecount.grid(column=2, row=7)


# ? how many sheets?
sheets_lable = ttk.Label(mainf, text="How many sheets of paper per signature do you want?").grid(
    column=0, row=9, sticky="w")
sheets = ttk.Combobox(mainf, textvariable=sig_thickness)
sheets['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16, 17, 18, 19, 20)
sheets.grid(column=0, row=10, sticky="W")
sheets.current(0)


num_sigs = ttk.Label(
    mainf, text="This makes this many full signatures: ").grid(column=1, row=10, sticky='e')
num_sigs_var = ttk.Label(mainf, textvariable=sig_count).grid(column=2, row=10)

page_persig = ttk.Label(mainf, text="each signature has this many pages: ").grid(
    column=1, row=11, sticky='e')
page_persig_var = ttk.Label(
    mainf, textvariable=sig_thickness_x4).grid(column=2, row=11)

num_remain = ttk.Label(mainf, text="with this many left over pages: ").grid(
    column=1, row=12, sticky='e')
num_remain_var = ttk.Label(
    mainf, textvariable=sig_remain).grid(column=2, row=12)


# ? pages to add at start
blanks_lable = ttk.Label(mainf, text='would you like some blank pages at the start?').grid(
    column=0, row=12, sticky='w')
blanks = ttk.Combobox(mainf, textvariable=blank_start)
blanks['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16, 17, 18, 19, 20)
blanks.grid(column=0, row=14, sticky='w')


new_count = ttk.Label(
    mainf, text="pagecount with added blank pages at start is ").grid(column=1, row=9)
new_count_number = ttk.Label(
    mainf, textvariable=newtotal).grid(column=2, row=9)


# ? last sig thickness

equal_lable = ttk.Label(
    mainf, text="Do you want the last signature to be an equal thickness\nto all the others, or to be as small as possible?")
equal_lable.grid(column=0, row=16, sticky='w')
equal_button = ttk.Checkbutton(
    mainf, text="same thickness", variable=equal_ends_sig)
equal_button.grid(column=0, row=18, sticky='w')
equal_button.state(['selected'])
equal_ends_sig.set(1)


addpageatend = ttk.Label(mainf, text="adding this many blank pages at end").grid(
    column=1, row=18, stick='e')
addpageatend_var = ttk.Label(
    mainf, textvariable=end_blank_pages).grid(column=2, row=18)

# ? choose a file destination
out_label = ttk.Label(mainf, text="Choose an output file")
out_label.grid(column=0, row=20, sticky="W")
out_path = tk.StringVar()
out_file = ttk.Button(mainf, text="Output file",
                      command=lambda: output_file())
out_file.grid(column=0, row=22, sticky="W")

pdfout_lable = ttk.Label(mainf, textvariable=pdf_output_path)
pdfout_lable.grid(column=0, row=24, sticky="W")


# ? Process the file button
process_button = ttk.Button(mainf, text="Go and do the thing!",
                            command=process_the_pdf)
process_button.grid(row=26, column=6, sticky="E")


exitbutton = ttk.Button(mainf, text="EXIT/cancel", command=root.quit)
exitbutton.grid(row=26, column=0, sticky="W")

for child in mainf.winfo_children():
    child.grid_configure(padx=5, pady=5)
exitbutton.focus()

root.mainloop()
