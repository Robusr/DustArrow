import sys

from PyQt5 import QtCore,QtOpenGL,QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QActionGroup, QLabel, QProgressBar,
                             QSpinBox, QFontComboBox, QDialog,QVBoxLayout)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QTextCharFormat, QFont, QPixmap

from ui_MainWindow import Ui_MainWindow


import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

matplotlib.use("Qt5Agg")


class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.figure = plt.figure() # 新建绘图区域
        self.canvas = FigureCanvasQTAgg(self.figure) # 绘图区域放到图层canvas之中
        self.ui.gridLayout.addWidget(self.canvas, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）

    def plot_test(self):
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)
        self.canvas.draw() # 这是关键



    