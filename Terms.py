
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(500, 350)

        #button to go back to sign up
        self.backBtn = QtWidgets.QPushButton(Dialog)
        self.backBtn.setGeometry(QtCore.QRect(210, 280, 101, 31))
        self.backBtn.setObjectName("backBtn")

        # code for terms
        self.title = QtWidgets.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(190, 30, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setUnderline(True)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.terms = QtWidgets.QLabel(Dialog)
        self.terms.setGeometry(QtCore.QRect(60, 80, 391, 181))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.terms.setFont(font)
        self.terms.setObjectName("terms")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.backBtn.clicked.connect(Dialog.hide)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.backBtn.setText(_translate("Dialog", "Back"))
        self.title.setText(_translate("Dialog", "Terms of Use"))
        self.terms.setText(_translate("Dialog", "The information provided by this app is meant\n"
" for advice only. \n"
"\n"
" It should not soley be used for making trades. \n"
"\n"
" The creator takes no liability for financial loss."))

# run gui
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

