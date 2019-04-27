from PyQt5 import QtCore, QtGui, QtWidgets
from Terms import Ui_Dialog
import pymysql


class Ui_MainWindow(object):

    def messageBox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()


    def login(self):
        email = self.uEnt.text()
        password = self.pEnt.text()
        conn=pymysql.connect(host="localhost", user = 'root', password ="", db = "hon")
        cur=conn.cursor()
        query = ("insert into signup(email, password) values(%s,%s)")
        data = cur.execute(query, (email, password))
        if(data):
            self.messageBox("Success", "You are signed up!")




    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")



        # register button
        self.regBtn = QtWidgets.QPushButton(self.centralwidget)
        self.regBtn.setGeometry(QtCore.QRect(250, 240, 75, 23))
        self.regBtn.setObjectName("signBtn")
        self.regBtn.clicked.connect(self.login)

        #enter uname
        self.uEnt = QtWidgets.QLineEdit(self.centralwidget)
        self.uEnt.setGeometry(QtCore.QRect(230, 110, 113, 20))
        self.uEnt.setObjectName("uEnt")

        #enter pword
        self.pEnt = QtWidgets.QLineEdit(self.centralwidget)
        self.pEnt.setGeometry(QtCore.QRect(230, 150, 113, 20))
        self.pEnt.setObjectName("pEnt")
        self.pEnt.setEchoMode(QtWidgets.QLineEdit.Password)

        #uname label
        self.uLab = QtWidgets.QLabel(self.centralwidget)
        self.uLab.setGeometry(QtCore.QRect(160, 110, 47, 13))
        self.uLab.setObjectName("uLab")

        #pword label
        self.pLab = QtWidgets.QLabel(self.centralwidget)
        self.pLab.setGeometry(QtCore.QRect(160, 150, 47, 13))
        self.pLab.setObjectName("pLab")

        #title
        self.logLab = QtWidgets.QLabel(self.centralwidget)
        self.logLab.setGeometry(QtCore.QRect(270, 70, 41, 20))
        self.logLab.setObjectName("logLab")

        #tos button
        self.tosBtn = QtWidgets.QPushButton(self.centralwidget)
        self.tosBtn.setGeometry(QtCore.QRect(230, 210, 111, 23))
        self.tosBtn.setObjectName("logBtn")

        #agree box
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(250, 180, 100, 17))
        self.checkBox.setObjectName("checkBox")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setFixedSize(550, 300)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Register"))
        self.regBtn.setText(_translate("MainWindow", "Register"))
        self.uLab.setText(_translate("MainWindow", "Username"))
        self.pLab.setText(_translate("MainWindow", "Password"))
        self.logLab.setText(_translate("MainWindow", "SignUp"))
        self.tosBtn.setText(_translate("MainWindow", "Terms of Service"))
        self.checkBox.setText(_translate("MainWindow", "Accept Terms"))

        self.tosBtn.clicked.connect(self.openTerms)

    # method to open the terms page
    def openTerms(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def save(self):
        username = self.uLab.text()
        password = self.pLab.text()
        return username, password



# run gui
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

