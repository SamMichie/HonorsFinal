import sys
import csv
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *






class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.setStyleSheet("plastique")



        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSortingEnabled(True)




        self.pushButtonLoad = QtWidgets.QPushButton("Load Portfolio",
            clicked=self.on_pushButtonLoad_clicked)

        self.pushButtonWrite = QtWidgets.QPushButton("Save Portfolio",
            clicked=self.on_pushButtonWrite_clicked)

        self.update = QtWidgets.QPushButton("Update", clicked = self.on_pushButtonUpdate_clicked )



        layoutVertical = QtWidgets.QVBoxLayout(self)
        layoutVertical.addWidget(self.tableView)
        layoutVertical.addWidget(self.pushButtonLoad)
        layoutVertical.addWidget(self.pushButtonWrite)

    def loadCsv(self, fileName):
        self.model.clear()
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)


                for i in range(0, 7):
                    self.model.setData(self.model.index(0, i), QBrush(Qt.gray), QtCore.Qt.BackgroundRole)


    def writeCsv(self, fileName):
        with open(fileName, "w") as fileOutput:
            writer = csv.writer(fileOutput, lineterminator='\n')
            print('rowCount->', self.model.rowCount())
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.item(rowNumber, columnNumber).text()
                    for columnNumber in range(self.model.columnCount())
                ]
                print('fields->', fields)
                writer.writerow(fields)

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        fileName, _ =  QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Open CSV"),
            QtCore.QDir.currentPath(), self.tr("CSV Files (*.csv)"))
        if fileName:
            self.writeCsv(fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        fileName, _ =  QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open CSV"),
            QtCore.QDir.currentPath(), self.tr("CSV Files (*.csv)"))

        if fileName:
            self.loadCsv(fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonUpdate_clicked(self):
        run()



class testWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(testWindow, self).__init__(parent)
        tabwidget = QtWidgets.QTabWidget()

        self.setCentralWidget(tabwidget)
        tabwidget.addTab(Widget(), "Options")
        tabwidget.addTab(Widget(), "Stocks")
        self.setFixedSize(800,478)
        testWindow.setWindowTitle(self, "Portfolio")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    app.setStyle('Fusion')
    main = testWindow()
    main.show()
    sys.exit(app.exec_())