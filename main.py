from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import os
import fitz
from PyQt5.QtGui import QIcon


class FileDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle("TOC Generator for PDF")
        self.setWindowIcon(QIcon('icon.png'))

        self.fileButton = QPushButton('Select PDF file', self)
        self.fileButton.clicked.connect(self.selectFile)

        self.tocFileButton = QPushButton('Select TOC file', self)
        self.tocFileButton.clicked.connect(self.selectTocFile)

        self.offsetLineEdit = QLineEdit(self)

        self.tocTableWidget = QTableWidget(0, 3, self)
        self.tocTableWidget.setHorizontalHeaderLabels(['Level', 'Title', 'Page'])
        self.tocTableWidget.verticalHeader().setDefaultSectionSize(20)
        self.tocTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.tocTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # self.tocTableWidget.verticalHeader().setVisible(False)
        self.tocTableWidget.horizontalHeader().setVisible(False)


        # width = self.tocTableWidget.width()
        # self.tocTableWidget.setColumnWidth(0, width * 0.2)
        # self.tocTableWidget.setColumnWidth(1, width * 0.6)
        # self.tocTableWidget.setColumnWidth(2, width * 0.2)
        

        self.indentPlusButton = QPushButton('+1', self)
        self.indentPlusButton.clicked.connect(self.increaseIndent)

        self.indentMinusButton = QPushButton('-1', self)
        self.indentMinusButton.clicked.connect(self.decreaseIndent)

        self.button = QPushButton('Add TOC', self)
        self.button.clicked.connect(self.addTOC)
        

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.fileButton)
        self.layout.addWidget(self.tocFileButton)
        self.layout.addWidget(QLabel('Enter page offset here (default 0):'))
        self.layout.addWidget(self.offsetLineEdit)
        self.layout.addWidget(QLabel('TOC preview:'))
        self.layout.addWidget(self.tocTableWidget)

        indentLayout = QHBoxLayout()
        indentLayout.addWidget(QLabel('Change level of selected item:'))
        indentLayout.addWidget(self.indentPlusButton)
        indentLayout.addWidget(self.indentMinusButton)
        self.layout.addLayout(indentLayout)

        self.layout.addWidget(self.button)
        
        # self.color_levels = [Qt.red, Qt.green, Qt.blue]
        self.color_levels = [QColor("#FFB6C1"), QColor("#ADD8E6"), QColor("#98FB98")]

    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select PDF file', '', 'PDF files (*.pdf)')
        if file_path:
            self.fileButton.setText(file_path)

    def selectTocFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select TOC file', '', 'Text files (*.txt)')
        if file_path:
            self.tocFileButton.setText(file_path)
            with open(file_path, 'r') as file:
                toc_text = file.read()
            self.tocTableWidget.setRowCount(0)
            for line in toc_text.split('\n'):
                try:
                    self.tocTableWidget.insertRow(self.tocTableWidget.rowCount())
                    line_info = line.split()
                    level, title, page = line_info[0], " ".join(line_info[1:-1]), line_info[-1]
                    
                    title = level + " " + title
                    level = str(1 + level.count("."))
                    # print(level)
                    self.tocTableWidget.horizontalHeader().setVisible(True)
                    self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 0, QTableWidgetItem(level))
                    self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 1, QTableWidgetItem(title))
                    self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 2, QTableWidgetItem(page))
                    
                    # width = self.tocTableWidget.viewport().size().width()
                    # self.tocTableWidget.setColumnWidth(0, width * 0.2)
                    self.tocTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                    # self.tocTableWidget.setColumnWidth(2, width * 0.2)
                    # self.tocTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
                except Exception as e:
                    QMessageBox.critical(None, f'Error at line {self.tocTableWidget.rowCount()}', f'Invalid offset {self.offsetLineEdit.text()}')
                    
            
            for i in range(self.tocTableWidget.rowCount()):
                level = int(self.tocTableWidget.item(i, 0).text())
                self.tocTableWidget.item(i, 0).setBackground(self.color_levels[level-1])
                
                

    def increaseIndent(self):
        for item in self.tocTableWidget.selectedItems():
            if item.column() == 0:
                level = int(item.text())
                if level < 3:
                    item.setText(str(level + 1))
                    item.setBackground(self.color_levels[level])
                

    def decreaseIndent(self):
        for item in self.tocTableWidget.selectedItems():
            if item.column() == 0:
                level = int(item.text())
                if level > 1:
                    item.setText(str(level - 1))
                    item.setBackground(self.color_levels[level-2])
                    

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith('.pdf'):
            self.fileButton.setText(file_path)
        elif file_path.endswith('.txt'):
            self.tocFileButton.setText(file_path)
            with open(file_path, 'r') as file:
                toc_text = file.read()
            self.tocTableWidget.setRowCount(0)
            for line in toc_text.split('\n'):
                self.tocTableWidget.insertRow(self.tocTableWidget.rowCount())
                level, title, page = line.split(',')
                self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 0, QTableWidgetItem(level))
                self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 1, QTableWidgetItem(title))
                self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 2, QTableWidgetItem(page))

    def addTOC(self):
        file_path = self.fileButton.text()
        # page_offset = int(self.offsetLineEdit.text()) if self.offsetLineEdit.text().isdecimal() else 0
        
        try:
            offset_str = self.offsetLineEdit.text()
            if offset_str == "":
                page_offset = 0
            else:
                page_offset = int(offset_str)
        except Exception as e:
            QMessageBox.critical(None, '', f'Error: invalid offset {self.offsetLineEdit.text()}')
        

        toc = []
        for i in range(self.tocTableWidget.rowCount()):
            level = int(self.tocTableWidget.item(i, 0).text())
            title = self.tocTableWidget.item(i, 1).text()
            page = int(self.tocTableWidget.item(i, 2).text()) + page_offset
            toc.append([level, title, page])
        # print(toc)
        
        output_dir = os.path.dirname(file_path)
        file_name_original = os.path.basename(file_path)
        output_file = os.path.join(output_dir, ".".join(file_name_original.split(".")[:-1]) + "_with_toc.pdf")
        try:
            self.add_toc_with_pymupdf(file_path, toc, output_file)
        except Exception as e:
            QMessageBox.critical(None, '', f'Error: {e}')
    
        QMessageBox.information(None, "", f"TOC added successfully!\nYou can find file in {output_file}")


    def add_toc_with_pymupdf(self, pdf_path, toc, output_path):
        doc = fitz.open(pdf_path)
        doc.set_toc(toc)
        doc.save(output_path)

app = QApplication([])
window = FileDropWidget()
window.show()
app.exec_()
