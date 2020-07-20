from PyPDF4 import PdfFileReader
from PyPDF4 import PdfFileWriter

test_file = r"C:\Users\user\Desktop\IMSLP456935-PMLP143602-Op.1_comb.pdf"

wfin = PdfFileReader(test_file)


def frasers2up(inputPdfFileWriter):

    edited_file = PdfFileWriter()
    blank_file = PdfFileWriter()
    leftpage = inputPdfFileWriter.getPage(0)
    leftx = leftpage.mediaBox.upperRight[0]
    lefty = leftpage.mediaBox.upperRight[1]

    for page in range(0, inputPdfFileWriter.getNumPages()-1, 2):
        leftpage = inputPdfFileWriter.getPage(page)
        rightpage = inputPdfFileWriter.getPage(page+1)
        leftx = leftpage.mediaBox.upperRight[0]
        lefty = leftpage.mediaBox.upperRight[1]

        # leftpage.mergeTranslatedPage(rightpage, leftx, 0, True)

        blank_file.insertBlankPage(leftx, lefty, 0)
        blank_page = blank_file.getPage(0)
        blank_page.mergeTranslatedPage(rightpage, leftx, 0, 1)
        blank_page.mergePage(leftpage)
        edited_file.addPage(blank_page)
    #     leftpage, leftx, 0, True)
    return edited_file


edited_file = frasers2up(wfin)

with open(r"C:\Users\user\Desktop\testoutput.pdf", 'w+b') as out_file:
    edited_file.write(out_file)
