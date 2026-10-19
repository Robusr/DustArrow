import sys

from PyQt5 import QtCore,QtOpenGL
from PyQt5.QtWidgets import (QApplication, QMainWindow, QActionGroup, QLabel, QProgressBar,
                             QSpinBox, QFontComboBox, QDialog)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QTextCharFormat, QFont, QPixmap

from ui_MainWindow import Ui_MainWindow

class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    