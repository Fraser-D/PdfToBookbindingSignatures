# using info from realpython.com and pypdf2

from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from PyPDF2 import PdfFileReader as Pdfread
from PyPDF2 import PdfFileWriter as Pdfwrite
from PyPDF2 import PdfFileMerger as Pdfmerge
import os
import math

# TODO get actual input file with gui or something for input


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

# ! NEEDS --> pdf_path, sig_thickness, blank_start, equal_ends_sig, pdf_output_path


def doallthestuff(pdf_path, sig_thickness, blank_start, equal_ends_sig, pdf_output_path):

    sig_thickness = int(sig_thickness)
    blank_start = int(blank_start)
    equal_ends_sig = int(equal_ends_sig)

    # pdf_path = r"C:\Users\user\PythonProjects\PdfToBookSignatures\multipage.pdf"
    # pdf_output_path = "testbookbindingpdf.pdf"
    # sig_thickness = int(input("how many sheets in each sig? "))
    # blank_start = int(input("how many blank pages at the begining? "))
    # equal_ends_sig = int(input('''
    # do you want the last sig to be same number of sheets
    # or as small as possible? 1 for same, 0 for small '''))

    # pdf = Pdfread(str(pdf_path))
    pdf = Pdfread(pdf_path)
    pdf_page_num = pdf.getNumPages()
    sheets_needed = math.ceil((pdf_page_num / 4))


# ! end of input


# all the page counting and padding

    pages_total = (blank_start + pdf_page_num)
    pages_per_sig = (sig_thickness * 4)
    sigs = (pages_total // pages_per_sig)
    page_remainder = (pages_total % pages_per_sig)

    if page_remainder == 0:
        blank_ends = 0
    elif sigs == 0:
        blank_ends = (pages_per_sig - pages_total)
    elif equal_ends_sig == 0:
        blank_ends = math.ceil(page_remainder / 4) * 4 - page_remainder
    else:
        blank_ends = (pages_per_sig - page_remainder)


# * this is the bit where we add blank pages and build the pdf, paper size is got
# * from the original file pdf. wf is where we do things
    wf = Pdfwrite()
    wf.appendPagesFromReader(pdf)

    for i in range(blank_start):
        wf.insertBlankPage(0)

    for i in range(blank_ends):
        wf.addBlankPage()


# * this is the sig shuffle bit, makes a list of the new page order

    list_pages = []

    for i in range(wf.getNumPages()):
        list_pages.append(i)

    def chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    list_sigs_pages = []
    for group in chunker(list_pages, pages_per_sig):
        list_sigs_pages.append(group)

    newpageorder = shufoutput(list_sigs_pages)

# ! wf - all the pdf and blank pages
# ! generate array of new page order

    newpdf = Pdfwrite()

    for page in newpageorder:
        newpdf.addPage(wf.getPage(page))

    wf = newpdf

# * this is the output part, turning them into 2up pdf output
# 2up based on code from https://github.com/mstamy2/PyPDF2/blob/master/Scripts/2-up.py

    wf_2up = Pdfwrite()
    for iter in range(0, wf.getNumPages()-1, 2):
        lhs = wf.getPage(iter)
        rhs = wf.getPage(iter+1)
        lhs.mergeTranslatedPage(rhs, lhs.mediaBox.getUpperRight_x(), 0, True)
        wf_2up.addPage(lhs)

    working_file = open(pdf_output_path, 'wb+')

    wf_2up.write(working_file)
    #
    working_file.close


# * this section is just outputting stats to the screen, page count etc

# print("\nthere are {} pages which needs {} sheets ({} blank pages at start)"
#       .format(pages_total, sheets_needed, blank_start))
# print("you want {} sheet per sig (with {} pages each)".format(
#     sig_thickness, (sig_thickness * 4)))
# print("there will be {} full sigs, with {} extra pages"
#       .format(sigs, page_remainder))
# if equal_ends_sig != 0:
#     print("this will need {} blank pages at end to have even sigs"
#           .format(blank_ends))
# else:
#     print("there will be {} blank pages at end, last sig will be {} papers"
#           .format(blank_ends, ((page_remainder + blank_ends) // 4)))

# print("total number of pages is {}".format(wf.getNumPages()))

# ! --> GUI section! woop

# ! NEEDS --> pdf_path, sig_thickness, blank_start, equal_ends_sig, pdf_output_path


def open_file():
    pdf_path_temp = filedialog.askopenfilename(
        title="Select a PDF file", filetypes=[("pdf files", ".PDF")]
    )
    pdf_path.set(pdf_path_temp)
    global glob_pdf_path
    glob_pdf_path = pdf_path_temp


def output_file():
    pdf_outpath_temp = filedialog.asksaveasfilename(
        title="Select a PDF file", filetypes=[("pdf files", ".PDF")], defaultextension=".pdf"
    )
    pdf_output_path.set(pdf_outpath_temp)
    global glob_pdf_output_path
    glob_pdf_output_path = pdf_outpath_temp


def process_the_pdf():
    confirm = tk.messagebox.askyesno(
        "Doing the thing", "Are you sure you want to do the thing?")
    if confirm == True:
        global glob_pdf_path
        global glob_sig_thickness
        glob_sig_thickness = str(sig_thickness.get())
        global glob_blank_start
        glob_blank_start = str(blank_start.get())
        global glob_equal_ends_sig
        glob_equal_ends_sig = str(equal_ends_sig.get())
        global glob_pdf_output_path
        try:
            doallthestuff(glob_pdf_path, glob_sig_thickness, glob_blank_start,
                          glob_equal_ends_sig, glob_pdf_output_path)
            messagebox.showinfo("Done!", "This may have worked! or not!")
        except FileNotFoundError:
            tk.messagebox.showerror(
                "File not found", "Either the input file or the output files is wrong.\nOr both of them. Who knows?")
            pass
    else:
        pass


root = tk.Tk()
root.title("Reorder PDF into Bookbinding Signatures for Duplex Printing")
mainf = ttk.Frame(root, padding="3 3 12 12")
mainf.grid(column=0, row=0, sticky=('N', "W", "S", 'E'))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

pdf_path = tk.Variable()
sig_thickness = tk.IntVar()
blank_start = tk.IntVar()
equal_ends_sig = tk.IntVar()
pdf_output_path = tk.Variable()


glob_pdf_path = ""
glob_sig_thickness = 1
glob_blank_start = 0
glob_equal_ends_sig = 1
glob_pdf_output_path = ""


title1 = ttk.Label(mainf, text="Pdf to Bookbinding Signatures")
title1.grid(column=0, row=0, sticky='W')
title2 = ttk.Label(
    mainf, text="A simple program for reordering the pages of a PDF file into bookbinding signatures for duplex printing")
title2.grid(column=0, row=2, sticky="w")

choose_label = ttk.Label(mainf, text="Choose a PDF file to work on")
choose_label.grid(column=0, row=4, sticky="W")
pdf_path = tk.StringVar()
input_file = ttk.Button(mainf, text="Choose file",
                        command=lambda: open_file())
input_file.grid(column=0, row=6, sticky="W")

pdf_lable = ttk.Label(mainf, textvariable=pdf_path)
pdf_lable.grid(column=0, row=7, sticky="W")

sheets_lable = ttk.Label(mainf, text="How many sheets of paper per signature do you want?").grid(
    column=0, row=9, sticky="w")
sheets = ttk.Combobox(mainf, textvariable=sig_thickness)
sheets['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16, 17, 18, 19, 20)
sheets.grid(column=0, row=10, sticky="W")
sheets.current(0)

blanks_lable = ttk.Label(mainf, text='would you like some blank pages at the start?').grid(
    column=0, row=12, sticky='w')
blanks = ttk.Combobox(mainf, textvariable=blank_start)
blanks['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16, 17, 18, 19, 20)
blanks.grid(column=0, row=14, sticky='w')

equal_lable = ttk.Label(
    mainf, text="Do you want the last signature to be an equal thickness to all the others,\nor to be as small as possible?")
equal_lable.grid(column=0, row=16, sticky='w')
equal_button = ttk.Checkbutton(
    mainf, text="same thickness", variable=equal_ends_sig, onvalue=1, offvalue=0)
equal_button.grid(column=0, row=18, sticky='w')
equal_button.state(['selected'])


out_label = ttk.Label(mainf, text="Choose an output file")
out_label.grid(column=0, row=20, sticky="W")
out_path = tk.StringVar()
out_file = ttk.Button(mainf, text="Choose file",
                      command=lambda: output_file())
out_file.grid(column=0, row=22, sticky="W")

pdfout_lable = ttk.Label(mainf, textvariable=pdf_output_path)
pdfout_lable.grid(column=0, row=24, sticky="W")


exitbutton = ttk.Button(mainf, text="EXIT/cancel", command=root.quit)
exitbutton.grid(row=26, column=0, sticky="W")

go_button = ttk.Button(mainf, text="Go and do the thing!",
                       command=process_the_pdf)
go_button.grid(row=26, column=6, sticky="E")

for child in mainf.winfo_children():
    child.grid_configure(padx=5, pady=5)
exitbutton.focus()

root.mainloop()
