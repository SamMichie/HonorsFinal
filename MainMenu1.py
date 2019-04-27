from PyQt5 import QtCore, QtGui, QtWidgets
from Terms import Ui_Dialog
from Hedging import Ui_Hedge
from Portfolio import testWindow

from stockloop import StockWindow1
from loop import MyWindow
from selectPrice import choose
from fin import App
from Rebalancing import BalanceWindow




class Ui_Dialog1(object):
    def setupUi(self, Dialog1):

        Dialog1.setObjectName("Main Menu")
        Dialog1.setFixedSize(484, 309)
        Dialog1.setStyleSheet("plastique")


        #button to take to hedging window
        self.hedgeBtn = QtWidgets.QPushButton(Dialog1)
        self.hedgeBtn.setGeometry(QtCore.QRect(30, 150, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.hedgeBtn.setFont(font)
        self.hedgeBtn.setStyleSheet("plastique")
        self.hedgeBtn.setObjectName("pushButton")
        self.hedgeBtn.clicked.connect(self.changeWindowH)

        #button to go to protfolio page
        self.portBtn = QtWidgets.QPushButton(Dialog1)
        self.portBtn.setGeometry(QtCore.QRect(30, 90, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        font.setItalic(False)
        self.portBtn.setFont(font)
        self.portBtn.setStyleSheet("plastique")
        self.portBtn.setObjectName("pushButton_3")
        self.portBtn.clicked.connect(self.changeWindowP)

        #button to go to stocks page
        self.stockBtn = QtWidgets.QPushButton(Dialog1)
        self.stockBtn.setGeometry(QtCore.QRect(30, 210, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.stockBtn.setFont(font)
        self.stockBtn.setStyleSheet("plastique")
        self.stockBtn.setObjectName("pushButton_4")
        self.stockBtn.clicked.connect(self.changeWinodwSP)

        # graph
        self.graph = QtWidgets.QPushButton(Dialog1)
        self.graph.setGeometry(QtCore.QRect(260, 90, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.graph.setFont(font)
        self.graph.setStyleSheet("plastique")
        self.graph.setObjectName("pushButton_6")
        self.graph.clicked.connect(self.changeWinodwGraph)

        # balance
        self.balance = QtWidgets.QPushButton(Dialog1)
        self.balance.setGeometry(QtCore.QRect(260, 150, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.balance.setFont(font)
        self.balance.setStyleSheet("plastique")
        self.balance.setObjectName("pushButton_6")
        self.balance.clicked.connect(self.changeWindowB)

        #logout close app
        self.exitBtn = QtWidgets.QPushButton(Dialog1)
        self.exitBtn.setGeometry(QtCore.QRect(260, 210, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.exitBtn.setFont(font)
        self.exitBtn.setStyleSheet("plastique")
        self.exitBtn.setObjectName("pushButton_5")
        self.exitBtn.clicked.connect(Dialog1.hide)

        self.label = QtWidgets.QLabel(Dialog1)
        self.label.setGeometry(QtCore.QRect(170, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog1)
        QtCore.QMetaObject.connectSlotsByName(Dialog1)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Main Menu"))
        self.hedgeBtn.setText(_translate("Dialog", "Option Pricing"))
        self.portBtn.setText(_translate("Dialog", "Portfolio"))
        self.stockBtn.setText(_translate("Dialog", "Stock Pricing"))
        self.graph.setText(_translate("Dialog", "Stock Graphs"))
        self.balance.setText(_translate("Dialog", "Balancing"))
        self.exitBtn.setText(_translate("Dialog", "Log Out"))
        self.label.setText(_translate("MainWindow", "Hedging System"))

    # mehtod to go to portfolio page
    def changeWindowP(self):
        self.window = testWindow()

        self.window.show()

    #go to balancing page
    def changeWindowB(self):
        self.window = BalanceWindow()

        self.window.show()

    # mehtod to go to pricing page
    def changeWindowH(self):
        self.window = choose()
        self.window.show()



    def changeWinodwSP(self):
        self.window = StockWindow1()
        self.window.show()

    def changeWinodwGraph(self):
        self.window = App()
        self.window.show()




# code to run gui
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Dialog1()
    Dialog1 = QtWidgets.QDialog()
    ui.setupUi(Dialog1)
    Dialog1.show()
    sys.exit(app.exec_())

