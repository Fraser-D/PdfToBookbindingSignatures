# PdfToBookbindingSignatures
Have a PDF you want to print out and bind? This program will take a pdf and reorder the pages into signatures for duplex printing.
You can choose how many sheets of paper you want per signature, if you want to add some blank pages at the start, and whether you want the final signature to be the same size as all the others or to be as small as possible. The program will automatically add the right amount of blank pages to the end of the book to make the signatures the right size.

It exports a pdf in 2up, ready for duplex printing.

PdfToBookSignaturesGUIv2.py is the working version, if you want to download and use it you will need PyPDF4 which you can get by running
`pip install PyPDF4` Once PyPDF4 is installed you can run the program using `python PdfToBookbindingSignatures.py` in the folder you downloaded it to.

This is a Python thing I made while learning how to code stuff, so it may be terrible. (But it does seem to be working!)

Now with super basic GUI in the gui one, some basic error handling (probably implemented wrong) and bugs!

Uses PyPDF4 and python 3

If you are using Windows there is a .exe that you can download in the ["/dist/" folder](https://github.com/Fraser-D/PdfToBookbindingSignatures/tree/master/dist), if you feel like trusting .exe files from the internet

The .exe is built from pdftobookbindingsignaturesGUIv2.py with `pyInstaller -F`
