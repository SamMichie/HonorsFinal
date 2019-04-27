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

df = pd.read_csv('OptionsPortfolio.csv')


class Option:
    def __init__(self, type, S, K, sigma, r, t, name, price1, gamma1, delta1, theta1, vega1, bPrice):
        self.type = type
        self.S = S
        self.K = K
        self.sigma = sigma
        self.r = r
        self.t = t
        self.name = name
        self.price1 = price1
        self.gamma1 = gamma1
        self.delta1 = delta1
        self.theta1 = theta1
        self.vega1 = vega1
        self.bPrice = bPrice


    def d1(self):
        """
        d1 term used in B.S. formula
        """
        numerator = math.log(self.S / self.K) + (self.r + (self.sigma * self.sigma) / 2.0) * self.t
        denom = self.sigma * math.sqrt(self.t)
        return numerator / denom

    def d2(self):
        """
        d2 term used in B.S. formula
        """
        return self.d1() - self.sigma * math.sqrt(self.t)

    def price(self):

        if (self.type == 'Put' or self.type == 'put' or self.type == 'P' or self.type == 'p'):

            """
            Return the price of a European Put Option using the Black-Scholes formula

            S: initial spot price of stock
            K: strike price of option
            sigma: volatility
            r: risk-free interest rate
            t: time to maturity (in years)
            """
            v1 = self.d1()
            v2 = self.d2()
            return format(self.K * math.exp(-self.r * self.t) * norm.cdf(-v2) - self.S * norm.cdf(-v1), '.4f')

        elif (self.type == 'Call' or self.type == 'c' or self.type == 'call' or self.type == 'C'):

            """
            Return the price of a European Call Option using the Black-Scholes formula

            S: initial spot price of stock
            K: strike price of option
            sigma: volatility
            r: risk-free interest rate
            t: time to maturity (in years)
            """
            v1 = self.d1()
            v2 = self.d2()
            return format(self.S * norm.cdf(v1) - self.K * math.exp(-self.r * self.t) * norm.cdf(v2), '.4f')
        else:
            print("error, check type your option type")

    def delta(self):
        q = float(4)
        T = float(5) / 365.0
        dfq = e ** (- q * T)

        if self.type == 'Call' or self.type == 'c' or self.type == 'call' or self.type == 'C':
            return format(dfq * norm.cdf(self.d1()), '.4f')
        else:
            return format(dfq * (norm.cdf(self.d1()) - 1), '.4f')

    def gamma(self):
        q = float(4)
        T = float(5) / 365.0
        sigmaT = self.sigma * T ** 0.5
        return format(e ** (q * T) * norm.pdf(self.d1()) / (self.S * sigmaT), '.4f')

    def vega(self):
        q = float(4)
        T = float(5) / 365.0
        return format(0.01 * self.S * e ** (- q * T) * \
                      norm.pdf(self.d1()) * T ** 0.5, '.4f')

    def theta(self):
        q = float(4)
        T = float(5) / 365.0
        df = e ** -(self.r * T)
        type1 = 0

        if self.type == 'Call' or self.type == 'c' or self.type == 'call' or self.type == 'C':
            type1 = 1

        else:
            type1 = 0

        dfq = e ** (- q * T)
        tmptheta = (1.0 / 365.0) \
                   * (-0.5 * self.S * dfq * norm.pdf(self.d1()) * \
                      self.sigma / (T ** 0.5) + \
                      type1 * (q * self.S * dfq * norm.cdf(type1 * self.d1()) \
                               - self.r * self.K * df * norm.cdf(type1 * self.d2())))
        return format(tmptheta, '.4f')

    def price2(self, div=0, n=100, am=False):
        if self.type == 'Call' or self.type == 'c' or self.type == 'call' or self.type == 'C':

            """
            Price a call option using the Binomial Options Pricing model

            S: initial spot price of stock
            K: strick price of option
            sigma: volatility
            r: risk-free interest rate
            t: time to maturity (in years)
            div: dividend yield (continuous compounding)
            n: binomial steps

            %timeit results: 10000 loops, best of 3: 139 us per loop
            """
            return self.option2(div, 1, n, am)

        elif (self.type == 'Put' or self.type == 'put' or self.type == 'P' or self.type == 'p'):

            """
            Price a put option using the Binomial Options Pricing model

            S: initial spot price of stock
            K: strick price of option
            sigma: volatility
            r: risk-free interest rate
            t: time to maturity (in years)
            div: dividend yield (continuous compounding)
            n: binomial steps

            %timeit results: 10000 loops, best of 3: 136 us per loop
            """
            return self.option2(div, -1, n, am)

    def option2(self, div=0, call=1, n=100, am=False):
        """
        Price an option using the Binomial Options Pricing model

        S: initial spot price of stock
        K: strick price of option
        sigma: volatility
        r: risk-free interest rate
        t: time to maturity (in years)
        div: dividend yield (continuous compounding)
        n: binomial steps
        """
        delta = float(self.t) / n
        u = math.exp(self.sigma * math.sqrt(delta))
        d = float(1) / u
        pu = float((math.exp((self.r - div) * delta) - d)) / (u - d)  # Prob. of up step
        pd = 1 - pu  # Prob. of down step
        u_squared = u * u
        S = self.S * pow(d, n)  # stock price at bottom node at last date
        prob = pow(pd, n)  # prob. of bottom node at last date
        opt_val = prob * max(0, call * (S - self.K))
        for i in range(1, n):
            S = S * u_squared
            prob = prob * (float(pu) / pd) * (n - i + 1) / i
            opt_val = opt_val + prob * max(call * (S - self.K), 0)
        return math.exp(-self.r * self.t) * opt_val






row_amount = len(df.index) #row amount

options = []

price = []
bPrice1 = []
gamma = []
delta = []
vega = []
theta = []

#TOTALS
gammaT = 0
deltaT = 0
vegaT = 0
thetaT = 0
priceT = 0
totalT = 0
callPutT = 0

count = 0
calls = 0


#creating option objects
for row in range(0, row_amount):
    option = Option(df.iloc[row, 1], df.iloc[row, 2], df.iloc[row, 3], df.iloc[row, 4], df.iloc[row, 5], df.iloc[row, 6], df.iloc[row,0], 0,0,0,0,0,0)
    options.append(option)

#calculating price
for i in range(len(options)):
    price.append(float(options[i].price()))

#calc gamma
for i in range(len(options)):
    gamma.append(float(options[i].gamma()))

#calc delta
for i in range(len(options)):
    delta.append(float(options[i].delta()))

#calc vega
for i in range(len(options)):
    vega.append(float(options[i].vega()))

#calc theta
for i in range(len(options)):
    theta.append(float(options[i].theta()))

#gamma total
for i in range(len(gamma)):
    gammaT += gamma[i]

#delta total
for i in range(len(delta)):
    deltaT += delta[i]

#theta total
for i in range(len(theta)):
    thetaT += theta[i]

#vega total
for i in range(len(vega)):
    vegaT += vega[i]

#price total
for i in range(len(price)):
    priceT += price[i]

#calculating price
for i in range(len(options)):
    for n in range(len(price)):
        options[i].price1 = price[i]

#calc gamma
for i in range(len(options)):
    for n in range(len(gamma)):
        options[i].gamma1 = gamma[i]

#calc delta
for i in range(len(options)):
    for n in range(len(delta)):
        options[i].delta1 = delta[i]

#calc theta
for i in range(len(options)):
    for n in range(len(theta)):
        options[i].theta1 = theta[i]

#calc vega
for i in range(len(options)):
    for n in range(len(vega)):
        options[i].vega1 = vega[i]

#total options
for i in range(len(options)):
    totalT += 1

#calculate binomial price
for i in range(len(options)):
    bPrice1.append(float(options[i].price2()))

#set price 2
for i in range(len(options)):
    for n in range(len(bPrice1)):
        options[i].bPrice = bPrice1[i]

#total count total
for i in range(len(options)):
   count += 1

#total count totalcall
for i in range(len(options)):
   if options[i].type == "Call":
       calls+=1

roundPrice = format(priceT, '.2f')
roundGamma = format(gammaT, '.5f')
roundDelta = format(deltaT, '.5f')
roundTheta = format(thetaT, '.5f')
roundVega = format(vegaT, '.5f')

#balancing
#b1 = gammaT / options[1].gamma1
gb = []
db = []
tb = []
vb = []

for i in range(len(options)):
    try:
        gb.append((gammaT)/(options[i].gamma1))
        db.append(deltaT/options[i].delta1)
        tb.append(thetaT/options[i].theta1)
        vb.append(vegaT/options[i].vega1)
    except ZeroDivisionError:
        gb.append(0)
        db.append(0)
        tb.append(0)
        vb.append(0)





class OptionTwo:
    def __init__(self, name1, type1, price2, balanceGamma, balanceDelta, balanceTheta, balanceVega):
        self.name1 = name1
        self.type1 = type1
        self.price2 = price2
        self.balanceGamma = balanceGamma
        self.balanceDelta = balanceDelta
        self.balanceTheta = balanceTheta
        self.balanceVega = balanceVega



ob1 = OptionTwo(options[1].name, options[1].type, options[1].price1, gb[1], db[1], tb[1], vb[1])
ob2 = OptionTwo(options[2].name, options[2].type, options[2].price1, gb[2], db[2], tb[2], vb[2])
ob3 = OptionTwo(options[3].name, options[3].type, options[3].price1, gb[3], db[3], tb[3], vb[3])
ob4 = OptionTwo(options[4].name, options[4].type, options[4].price1, gb[4], db[4], tb[4], vb[4])
ob5 = OptionTwo(options[5].name, options[5].type, options[5].price1, gb[5], db[5], tb[5], vb[5])
ob6 = OptionTwo(options[6].name, options[6].type, options[6].price1, gb[6], db[6], tb[6], vb[6])
ob7 = OptionTwo(options[7].name, options[7].type, options[7].price1, gb[7], db[7], tb[7], vb[7])
ob8 = OptionTwo(options[8].name, options[8].type, options[8].price1, gb[8], db[8], tb[8], vb[8])
ob9 = OptionTwo(options[9].name, options[9].type, options[9].price1, gb[9], db[9], tb[9], vb[9])
ob10 = OptionTwo(options[10].name, options[10].type, options[10].price1, gb[10], db[10], tb[10], vb[10])

balanceOptions = []

balanceOptions.append(ob1)
balanceOptions.append(ob2)
balanceOptions.append(ob3)
balanceOptions.append(ob4)
balanceOptions.append(ob5)
balanceOptions.append(ob6)
balanceOptions.append(ob7)
balanceOptions.append(ob8)
balanceOptions.append(ob9)
balanceOptions.append(ob10)

with open('balance.csv', 'w', newline='') as csvfile:
    fieldnames = ['name1', 'type1', 'price2', 'balanceGamma', 'balanceDelta', 'balanceTheta', 'balanceVega']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for i in balanceOptions:
        writer.writerow(vars(i))




####################################### GUI #######################################################
#gui window
class BalanceWindow(QWidget):
    def __init__(self, parent=None):
        super(BalanceWindow, self).__init__(parent)
        BalanceWindow.update(self)

        BalanceWindow.setFixedSize(self, 800, 500)
        BalanceWindow.setWindowTitle(self, "Balance")

        self.fileName = r'C:\Users\sammi\PycharmProjects\Honours\balance.csv'
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

        for i in range(1, 2):
            self.model2.setData(self.model2.index(i, 3), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 0), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 1), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 2), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 4), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 5), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 6), QBrush(Qt.green), QtCore.Qt.BackgroundRole)
            self.model2.setData(self.model2.index(i, 7), QBrush(Qt.green), QtCore.Qt.BackgroundRole)





        self.layoutVertical = QVBoxLayout(self)

        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.view)
        #self.layoutVertical.addWidget(self.select)

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



    @pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)


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

    main = BalanceWindow()
    main.show()

    sys.exit(app.exec_())


















