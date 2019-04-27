import math
from scipy.stats import norm
import csv
import pandas as pd
import sys
from math import e
import csv
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from iex import Stock
import operator

df = pd.read_csv('StocksPortfolio.csv')


class UserStock:
    def __init__(self, name, amount, cps, total, price1, currentTotal, return1, percentage_return):
        self.name = name
        self.amount = amount
        self.cps = cps
        self.total = total
        self.price1 = price1
        self.currentTotal = currentTotal
        self.return1 = return1
        self.percentage_return = percentage_return

    def calcTotal(self):
        return float(self.amount * self.cps)

    def calcPrice(self):
        return (Stock(self.name).price())

    def calcCurrentT(self):
        return format(float(self.price1 * self.amount), '.4f')

    def calcReturn(self):
        return format(float(self.currentTotal - self.price1), '.4f')

    def calcPR(self):
        return format(((self.return1/self.currentTotal)*100), '.4f')



row_amount = len(df.index) #total rows

stockList = []
calcTotal1 = []
calcPrice1 = []
calcCurrentTotal = []
calcReturn1 = []
calcP = []

for row in range(0, row_amount):
    stock1 = UserStock(df.iloc[row, 0], df.iloc[row, 1], df.iloc[row, 2], 0, 0, 0, 0, 0)
    stockList.append(stock1)

#calc total
for i in range(len(stockList)):
    calcTotal1.append(float(stockList[i].calcTotal()))

#set total
for i in range(len(stockList)):
    for n in range(len(calcTotal1)):
        stockList[i].total = calcTotal1[i]

#calc price using API
for i in range(len(stockList)):
    calcPrice1.append(float(stockList[i].calcPrice()))

#set price
for i in range(len(stockList)):
    for n in range(len(calcPrice1)):
        stockList[i].price1 = calcPrice1[i]

#calc current total
for i in range(len(stockList)):
    calcCurrentTotal.append(float(stockList[i].calcCurrentT()))

#set CT
for i in range(len(stockList)):
    for n in range(len(calcCurrentTotal)):
        stockList[i].currentTotal = calcCurrentTotal[i]

# calc return
for i in range(len(stockList)):
    calcReturn1.append(float(stockList[i].calcReturn()))

# set return
for i in range(len(stockList)):
    for n in range(len(calcReturn1)):
        stockList[i].return1 = calcReturn1[i]

# calc percentage
for i in range(len(stockList)):
    calcP.append(float(stockList[i].calcPR()))

# set percentage
for i in range(len(stockList)):
    for n in range(len(calcP)):
        stockList[i].percentage_return = calcP[i]

print(stockList[1].return1)

#load stocks into csv
with open('stockTest.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'amount', 'cps', 'total', 'price1', 'currentTotal','return1', 'percentage_return']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for i in stockList:
        writer.writerow(vars(i))



####################### GUI #######################

class StockWindow1(QWidget):
    def __init__(self, parent=None):
        super(StockWindow1, self).__init__(parent)
        StockWindow1.update(self)
        StockWindow1.setWindowTitle(self, "Stock Pricing")


        self.fileName = r'C:\Users\sammi\PycharmProjects\Honours\stockTest.csv'

        StockWindow1.setFixedSize(self, 900, 373)

        self.model = QStandardItemModel(self)

        # self.model.setHorizontalHeaderLabels(['Name', 'Type', 'Price'])

        self.tableView = QTableView(self)
        self.tableView.setSortingEnabled(True)

        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.on_pushButtonLoad_clicked()

        for i in range(0, 8):
            self.model.setData(self.model.index(0, i), QBrush(Qt.gray), QtCore.Qt.BackgroundRole)


        # self.loadCsv(r'C:\Users\sammi\PycharmProjects\Honours\test1.csv')

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)

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

    def writeCsv(self, fileName):
        with open(fileName, "w") as fileOutput:
            writer = csv.writer(fileOutput, lineterminator='\n')
            print('rowCount->', self.model.rowCount())
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                print('fields->', fields)
                writer.writerow(fields)

    @pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    ##########################################
    def sort(self, Ncol, order):
        """Sort table by given column number."""
        self.layoutAboutToBeChanged.emit()
        self.data = self.data.sort_values(self.headers[Ncol],
                                          ascending=order == Qt.AscendingOrder)
        self.layoutChanged.emit()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    app.setStyle('Fusion')

    main = StockWindow1()
    main.show()

    sys.exit(app.exec_())











