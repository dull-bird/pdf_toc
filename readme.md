# A PDF TOC Generator

## Introduction

We often find some PDF files do not have a table of content (TOC), which makes it inconvenient for us to read the file, especially for books. I build this tool to help you to generate one TOC. To do this, you need:

1. a PDF file.
2. a TOC file (.txt), containing the TOC information in such a format:

```
level title page 
```

```
1 title 1 1
1.1 title 2 2
1.2 title 3 3
1.2.1 title 4 4
2 title 5 10
```

Only three-level titles are supported.

Since sometimes the TOC file may not be fully correct (some typo when you copy the text from the pdf files), I implement a preview panel so you can preview and edit the level (can be done easily by clicking the "+1" and "-1" button), title, or the page number in the panel.

The tool supports a page offset which will be added to the pages in the TOC file (an positive or negative integer, default 0).

## Requirements
- python 3
- PyQt5 and PyMuPDF installed

## Usuage

Go to the folder containing main.py, run
```
python main.py
```

A window will show
<img src="./screenshot/main_window.png" alt="alt text" style="width:50%;">

You can run test:
<img src="./screenshot/test.png" alt="alt text" style="width:50%;">

And the output file will be saved in the same folder with the original PDF file.