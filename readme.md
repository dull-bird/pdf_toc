# A PDF Table of Contents Generator

English | [中文版](readme_cn.md)
## Introduction

We often find some PDF files do not have a table of contents (TOC), which makes it inconvenient for us to read the file, especially for books. I build this tool to help you to generate one TOC. To do this, you need:

1. a PDF file.
2. a TOC file (.txt), containing the TOC information in such a format:

```
level title page
```

An example:

```
1 title 1 1
1.1 title 2 2
1.2 title 3 3
1.2.1 title 4 4
2 title 5 10
```

Note:

- Any level titles are supported now.
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/document.html#Document.set_toc) has some rules of TOC:
  - It will delete the previous TOC and create a new one.
  - level is a integer (> 0) which must be 1 for the first item and **at most 1 larger than the previous one**.
  - page can be set to -1 if there is no target, or the target is external.

Since sometimes the TOC file may not be fully correct (some typo when you copy the text from the pdf files), I implement a preview panel so you can preview and edit the level (can be done easily by clicking the "+1" and "-1" button), title, or the page number in the panel.

The tool supports a page offset which will be added to the pages in the TOC file (an positive or negative integer, default 0).

## Features

- An editing panel to adjust title, level and page
- Support any level contents
- Ignore empty lines in the TOC (.txt) file
- Highlight (with red background) invalid (non-integer) page numbers and invalid levels (non-integer or smaller than 1), and stop adding the TOC if they are detected

## Requirements

- python 3 (>=3.8) (other versions may also work)
- PyQt5 (>=5.9.2) and PyMuPDF (>=1.22.5) installed (other versions may also work)

## Installation

- Install Python
- Create a virtual environment and activate it

    ```powershell
    python -m venv .venv

    .\.venv\Scripts\Activate.ps1 # Windows Powershell
    # source .venv/bin/activate # Linux

    ```

- Install Dependencies

    ```powershell
    pip install -r requirements.txt
    ```


## Usuage

- First download the git repository (you can simply download the zip file and unzip it).
- Go to the folder containing main.py, and run

```
python main.py
```

A window will show:

<img src="./screenshot/main_window.png" alt="alt text" style="width:50%;">

You can run test:

<img src="./screenshot/test.png" alt="alt text" style="width:50%;">

And the output file will be saved in the same folder with the original PDF file.
