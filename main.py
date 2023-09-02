import math
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QBrush
import os
import fitz
from PyQt5.QtGui import QIcon

# def on_item_clicked(item):
    # table = QApplication.instance().sender()
    # selected_indexes = table.selectedIndexes()
    # # 如果点击的项已经被选中，取消选中
    # if any([idx.row() == item.row() and idx.column() == item.column() for idx in selected_indexes]):
    #     table.clearSelection()
    # else:
    #     table.selectRow(item.row())
        

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.last_clicked_item = None
        
        self.setAcceptDrops(True)
        self.setWindowTitle("TOC Generator for PDF")
        self.setWindowIcon(QIcon('icon.png'))

        self.fileButton = QPushButton('Select/drop PDF file', self)
        self.fileButton.clicked.connect(self.selectFile)

        self.tocFileButton = QPushButton('Select/drop TOC file', self)
        self.tocFileButton.clicked.connect(self.selectTocFile)

        self.offsetLineEdit = QLineEdit(self)

        self.tocTableWidget = QTableWidget(0, 3, self)
        
        font = QFont()
        font.setFamily("Arial, Hei, Microsoft YaHei, sans-serif")
        self.tocTableWidget.setFont(font)
        
        self.tocTableWidget.setHorizontalHeaderLabels(['Level', 'Title', 'Page'])
        self.tocTableWidget.verticalHeader().setDefaultSectionSize(20)
        self.tocTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.tocTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # self.tocTableWidget.verticalHeader().setVisible(False)
        self.tocTableWidget.horizontalHeader().setVisible(False)
        self.tocTableWidget.setStyleSheet("""
            QTableView::item:selected {
                background-color: white;
                color: black;
                border: 2px solid DodgerBlue;
            }
            QTableView::item:selected:active {
                background-color: white;
                border: 2px solid DodgerBlue;
            }
            """)
        self.tocTableWidget.itemClicked.connect(self.on_item_clicked)
        # self.tocTableWidget.verticalHeader().sectionClicked.connect(self.on_item_or_header_clicked)
        # self.tocTableWidget.horizontalHeader().sectionClicked.connect(self.on_item_or_header_clicked)
        self.tocTableWidget.verticalHeader().setSectionsClickable(False)
        self.tocTableWidget.horizontalHeader().setSectionsClickable(False)
        self.tocTableWidget.cellChanged.connect(self.handle_cell_changed)


        
        # self.tocTableWidget.itemSelectionChanged.connect(self.handle_item_selection)


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
        self.color_levels = [QColor("#FFB6C1"), QColor("#ADD8E6"), QColor("#98FB98"), QColor("#D3D3D3"), QColor("#808080")]
        
    # def on_item_or_header_clicked(self, index_or_item):
    #     # 如果点击的是表头，取消所有选中的项目
    #     if isinstance(index_or_item, int):
    #         self.tocTableWidget.clearSelection()
    #         return

    #     # 处理项目点击逻辑
    #     item = index_or_item
    #     selected_indexes = self.tocTableWidget.selectedIndexes()
    #     is_already_selected = any([idx.row() == item.row() and idx.column() == item.column() for idx in selected_indexes])
    #     if is_already_selected and self.last_clicked_item == item:
    #         self.tocTableWidget.clearSelection()
    #         self.last_clicked_item = None
    #     else:
    #         self.last_clicked_item = item
    
    def handle_cell_changed(self, row, column):
        item = self.tocTableWidget.item(row, column)
        if item is not None:
            new_value = item.text()
            # print(f"Cell ({row}, {column}) changed to: {new_value}")
            if column == 0:
                if (not self.is_int(new_value) or not (1 <= int(new_value) <= math.inf)):
                    item.setBackground(QColor("red"))
                else:
                    item.setBackground(self.color_levels[min(int(new_value)-1, len(self.color_levels)-1)])
            
            if column == 2:
                if not self.is_int(new_value):
                    item.setBackground(QColor("red"))
                else:
                    item.setBackground(QBrush())
    
    def on_item_clicked(self, item):
        selected_indexes = self.tocTableWidget.selectedIndexes()
        
        # 检查此项是否在选中的列表中
        is_already_selected = any([idx.row() == item.row() and idx.column() == item.column() for idx in selected_indexes])

        # 如果此项已经被选中，并且它是上次点击的项
        if is_already_selected and self.last_clicked_item == item:
            self.tocTableWidget.clearSelection()
            self.last_clicked_item = None
        else:
            self.last_clicked_item = item
    
    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select PDF file', '', 'PDF files (*.pdf)')
        if file_path:
            self.fileButton.setText(file_path)

    def selectTocFile(self):
        """
        Open a file dialog to select a TOC file.

        This function opens a file dialog to allow the user to select a TOC (Table of Contents) file. The selected file path is then displayed on a button in the UI. Additionally, the function calls the `loadTocTable` method to load and display the contents of the selected TOC file in a table.

        Parameters:
            None

        Returns:
            None
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select TOC file', '', 'Text files (*.txt)')
        if file_path:
            self.tocFileButton.setText(file_path)
            self.loadTocTable(file_path)
    
    def loadTocTable(self, file_path):
        with open(file_path, 'r') as file:
            toc_text = file.read()
        self.tocTableWidget.setRowCount(0)
        for line in toc_text.split('\n'):
            if line == "":
                continue
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
                QMessageBox.critical(None, f'Error at line {self.tocTableWidget.rowCount()}', f'Invalid format: {line}')
                
            # for i in range(self.tocTableWidget.rowCount()):
                # level = int(self.tocTableWidget.item(i, 0).text())
                # self.tocTableWidget.item(i, 0).setBackground(self.color_levels[level-1])
                # if not self.is_int(self.tocTableWidget.item(i, 2).text()):
                    # self.tocTableWidget.item(i, 2).setBackground(QColor("#D3D3D3"))
                    
                
    @staticmethod 
    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def increaseIndent(self):
        for item in self.tocTableWidget.selectedItems():
            if item.column() == 0:
                level = int(item.text())
                if level < math.inf:
                    item.setText(str(level + 1))
                    # item.setBackground(self.color_levels[level])
                    
    
                

    def decreaseIndent(self):
        for item in self.tocTableWidget.selectedItems():
            if item.column() == 0:
                level = int(item.text())
                if level > 1:
                    item.setText(str(level - 1))
                    # item.setBackground(self.color_levels[level-2])
                    

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
            self.loadTocTable(file_path)
            
            # with open(file_path, 'r') as file:
            #     toc_text = file.read()
            # self.tocTableWidget.setRowCount(0)
            # for line in toc_text.split('\n'):
            #     self.tocTableWidget.insertRow(self.tocTableWidget.rowCount())
            #     level, title, page = line.split(',')
            #     self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 0, QTableWidgetItem(level))
            #     self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 1, QTableWidgetItem(title))
            #     self.tocTableWidget.setItem(self.tocTableWidget.rowCount() - 1, 2, QTableWidgetItem(page))

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
            try:
                assert 1 <= int(level) <= math.inf
            except Exception as e:
                QMessageBox.critical(None, '', f'Error: invalid level {self.tocTableWidget.item(i, 0).text()}')
                toc = []
                return
            
            title = self.tocTableWidget.item(i, 1).text()
            try:
                page = int(self.tocTableWidget.item(i, 2).text()) + page_offset
            except Exception as e:
                QMessageBox.critical(None, '', f'Error: invalid page number {self.tocTableWidget.item(i, 2).text()}')
                toc = []
                return
            toc.append([level, title, page])
        # print(toc)
        
        output_dir = os.path.dirname(file_path)
        file_name_original = os.path.basename(file_path)
        output_file = os.path.join(output_dir, ".".join(file_name_original.split(".")[:-1]) + "_with_toc.pdf")
        try:
            self.add_toc_with_pymupdf(file_path, toc, output_file)
            QMessageBox.information(None, "", f"TOC added successfully!\nYou can find file in {output_file}")
        except Exception as e:
            QMessageBox.critical(None, '', f'Error: {e}')
        


    def add_toc_with_pymupdf(self, pdf_path, toc, output_path):
        doc = fitz.open(pdf_path)
        doc.set_toc(toc)
        doc.save(output_path)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWidget()
    window.show()
    app.exec_()
