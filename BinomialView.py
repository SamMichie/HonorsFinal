import math
from scipy.stats import norm
import csv
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets  # works for pyqt5
import sys
from math import e
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#gui window
class MyWindowB(QWidget):
    def __init__(self, parent=None):
        super(MyWindowB, self).__init__(parent)
        MyWindowB.update(self)

        MyWindowB.setFixedSize(self, 800, 500)

        self.fileName = r'C:\Users\sammi\PycharmProjects\Honours\binomial.csv'
        self.totalsFile = r'C:\Users\sammi\PycharmProjects\Honours\totals.csv'





        self.model = QStandardItemModel(self)

        self.view = QTableView(self)
        self.model2 = QStandardItemModel(self)
        self.view.setModel(self.model2)
        #self.view.horizontalHeader().setStretchLastSection(True)




        # self.model.setHorizontalHeaderLabels(['Name', 'Type', 'Price'])

        self.tableView = QTableView(self)
        self.tableView.setSortingEnabled(True)

        self.view.setFixedSize(800,82)


        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)



        self.on_pushButtonLoad_clicked()
        self.on_pushButtonLoad_clicked1()

        # self.loadCsv(r'C:\Users\sammi\PycharmProjects\Honours\test1.csv')

        for i in range(0, 7):
            self.model.setData(self.model.index(0, i), QBrush(Qt.gray), QtCore.Qt.BackgroundRole)

        for i in range(0, 20):
            self.model.setData(self.model.index(i, 0), QBrush(Qt.gray), QtCore.Qt.BackgroundRole)

        self.layoutVertical = QVBoxLayout(self)

        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.view)


    def loadCsv(self, fileName):
        self.model.clear()
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)



    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open CSV"),
                                                            QtCore.QDir.currentPath(), self.tr("CSV Files (*.csv)"))

        if fileName:
            self.loadCsv(fileName)


    #binomail pricing
    @pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    def binomial_model(N, S0, u, r, K):
        """
        N = number of binomial iterations
        S0 = initial stock price
        u = factor change of upstate
        r = risk free interest rate per annum
        K = strike price
        """
        d = 1 / u
        p = (1 + r - d) / (u - d)
        q = 1 - p

        # make stock price tree
        stock = np.zeros([N + 1, N + 1])
        for i in range(N + 1):
            for j in range(i + 1):
                stock[j, i] = S0 * (u ** (i - j)) * (d ** j)

        # Generate option prices recursively
        option = np.zeros([N + 1, N + 1])
        option[:, N] = np.maximum(np.zeros(N + 1), (stock[:, N] - K))
        for i in range(N - 1, -1, -1):
            for j in range(0, i + 1):
                option[j, i] = (
                        1 / (1 + r) * (p * option[j, i + 1] + q * option[j + 1, i + 1])
                )
        return option
######################################################
    def loadCsv1(self, totalsFile):
        self.model2.clear()
        with open(totalsFile, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model2.appendRow(items)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked1(self):
        totalsFile, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open CSV"),
                                                            QtCore.QDir.currentPath(), self.tr("CSV Files (*.csv)"))

        if totalsFile:
            self.loadCsv1(totalsFile)

    @pyqtSlot()
    def on_pushButtonLoad_clicked1(self):
        self.loadCsv1(self.totalsFile)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    app.setStyle('Fusion')

    main = MyWindowB()
    main.show()

    sys.exit(app.exec_())