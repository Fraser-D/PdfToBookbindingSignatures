
# ! things that is the plan!
# import pdf, reorder pages so that standard duplex printing make book signatures
# import pdf
# ask about how many sheets to a signature is wanted
# add extra blank pages to the start and/or end if needed
# option for adding blank pages at the end OR having the last signature smaller than the others
# chop the pdf into individual pages, re order them, stitch back together
# using info from realpython.com and pypdf2

from PyPDF2 import PdfFileReader as Pdfread
from PyPDF2 import PdfFileWriter as Pdfwrite
from PyPDF2 import PdfFileMerger as Pdfmerge
import os
import math

# TODO get actual input file with gui or something for input
pdf_path = r"C:\Users\user\PythonProjects\PdfToBookSignatures\multipage.pdf"

pdf = Pdfread(str(pdf_path))

pdf_page_num = pdf.getNumPages()
sheets_needed = math.ceil((pdf_page_num / 4))

# ? how many sheets per sig
sig_thickness = int(input("how many sheets in each sig? "))
# sig_thickness = 1

# ? how many blank pages at start
blank_start = int(input("how many blank pages at the begining? "))
# blank_start = 1

# ? do you want all sigs to be equal
equal_ens_sig = int(input('''
do you want the last sig to be same number of sheets
or as small as possible? 1 for same, 0 for small '''))

# all the page counting and padding

pages_total = (blank_start + pdf_page_num)
pages_per_sig = (sig_thickness * 4)
sigs = (pages_total // pages_per_sig)
page_remainder = (pages_total % pages_per_sig)

if page_remainder == 0:
    blank_ends = 0
elif sigs == 0:
    blank_ends = (pages_per_sig - pages_total)
elif equal_ens_sig == 0:
    blank_ends = (4 - page_remainder)
else:
    blank_ends = (pages_per_sig - page_remainder)

# will need to get pages from the remainder and combine with blank pages
# or get them and treat them specially
# ! page numbers must be mod 4


# * this is the bit where we add blank pages and build the pdf, paper size is got
# * from the original file pdf. wf is where we do things
wf = Pdfwrite()
wf.appendPagesFromReader(pdf)

for i in range(blank_start):
    wf.insertBlankPage(0)

for i in range(blank_ends):
    wf.addBlankPage()


# * this is the sig shuffle bit - deal with end bits later

sort_sigs_array = []
if equal_ens_sig != 0:
    insigs = wf.getNumPages()
else:
    insigs = (wf.getNumPages() - page_remainder - blank_ends)

# leftovers = pages - insigs
for i in range(insigs):
    sort_sigs_array.append(i)


# ! wf - all the pdf and blank pages
# ! generate array of new page order
# ! loop over with:
# ! getPage -> PageObject
# ! addPage -> into the writer for output doc


# * this is the output part, turning them into 2up pdf output
# rotatororat based on code from https://github.com/mstamy2/PyPDF2/blob/master/Scripts/2-up.py

wf_2up = Pdfwrite()
for iter in range(0, wf.getNumPages()-1, 2):
    lhs = wf.getPage(iter)
    rhs = wf.getPage(iter+1)
    lhs.mergeTranslatedPage(rhs, lhs.mediaBox.getUpperRight_x(), 0, True)
    wf_2up.addPage(lhs)


working_file = open("testbookbindingpdf.pdf", 'wb+')

wf_2up.write(working_file)
#
working_file.close


# * this section is just outputting stats to the screen, page count etc

print("\nthere are {} pages which needs {} sheets ({} blank pages at start)"
      .format(pages_total, sheets_needed, blank_start))
print("you want {} sheet per sig (with {} pages each)".format(
    sig_thickness, (sig_thickness * 4)))
print("there will be {} full sigs, with {} extra pages"
      .format(sigs, page_remainder))
if equal_ens_sig != 0:
    print("this will need {} blank pages at end to have even sigs"
          .format(blank_ends))
else:
    print("there will be {} blank pages at end, last sig will be {} papers"
          .format(blank_ends, ((page_remainder + blank_ends) // 4)))

print("total number of pages is {}".format(wf.getNumPages()))
