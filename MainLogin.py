from PyQt5 import QtCore, QtGui, QtWidgets #works for pyqt5
import sys
from SignUp import Ui_MainWindow
from MainMenu1 import Ui_Dialog1
import pymysql


class Window(QtWidgets.QMainWindow):

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def warning(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()


    def login(self):
        username = self.uEnt.text()
        pword = self.pEnt.text()
        conn=pymysql.connect(host="localhost", user = 'root', password = "", db="hon")
        cur = conn.cursor()
        query = "select * from signup where email=%s and password=%s"
        data = cur.execute(query, (username, pword))
        if(len(cur.fetchall())>0):
            self.messagebox("congrats", "You are now Logged in!")
            self.changeWindow2()
            self.hide()
        else:
            self.warning("Denied", "Incorrect Username or Password, Try Again!")

    def __init__(self):
        super(Window, self).__init__()
        #self.setGeometry(0, 0, 550, 400)
        self.setFixedSize(550,400)
        self.setWindowTitle("Hedging Tool Login")
        self.setStyleSheet("plastique")




        self.home()

    def home(self):

        # the login page

        #enter username
        self.uEnt = QtWidgets.QLineEdit(self)
        self.uEnt.setGeometry(QtCore.QRect(230, 110, 113, 20))

        #enter password
        self.pEnt = QtWidgets.QLineEdit(self)
        self.pEnt.setGeometry(QtCore.QRect(230, 150, 113, 20))
        self.pEnt.setEchoMode(QtWidgets.QLineEdit.Password)


        #username label
        self.uLab = QtWidgets.QLabel("Username", self)
        self.uLab.setGeometry(QtCore.QRect(160, 110, 47, 13))

        #pass label
        self.pLab = QtWidgets.QLabel("Password", self)
        self.pLab.setGeometry(QtCore.QRect(160, 150, 47, 13))

        #title
        self.logLab = QtWidgets.QLabel("Login", self)
        self.logLab.setGeometry(QtCore.QRect(270, 70, 31, 16))

        #login button
        self.logBtn = QtWidgets.QPushButton("Login", self)
        self.logBtn.clicked.connect(self.login)
        self.logBtn.setGeometry(QtCore.QRect(280, 190, 75, 23))

        #signup button
        self.signBtn = QtWidgets.QPushButton("Sign Up", self)
        self.signBtn.clicked.connect(self.changeWindow)
        self.signBtn.setGeometry(QtCore.QRect(200, 190, 75, 23))

        self.show()

    # exit
    def close_app(self):
        sys.exit()

    # method to go to sign up page
    def changeWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    # method to go to menu after logging in
    def changeWindow2(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog1()
        self.ui.setupUi(self.window)
        self.window.show()
        self.destroy()


    # code for login system
    def logUandP(self):
        if (self.uEnt.text() == 'sam' and
                self.pEnt.text() == 'pass'):
            self.changeWindow2()
            self.hide()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')



# run gui
def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    GUI = Window()
    sys.exit(app.exec_())

run()



