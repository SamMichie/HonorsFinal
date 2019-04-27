import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import sys
import random
from stockloop import stockList

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from StockPricing import *




# stock data to plot
style.use("ggplot")
start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()
df = web.DataReader(s2.name, 'iex', start, end)
df.to_csv('tsla.csv')


df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
#print(df.head())

df['close'].plot()



class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):

        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=8, height=5)
        m.move(20, 20)

        choice = QComboBox(self)
        choice.move(5,5)

        #update button
        selectBtn = QPushButton(self)
        selectBtn.setText("Update")
        selectBtn.move(120,5)

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(choice)
        self.layoutVertical.addWidget(selectBtn)

        #loading stocks to combo box
        for i in range(len(stockList)):
            choice.addItem(stockList[i].name)


        self.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    # plotting data
    def plot(self):
        data = df['close']

        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('TESLA Stock Price History')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



