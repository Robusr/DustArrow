import sys
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QActionGroup, QLabel, QProgressBar,QMessageBox,
                             QSpinBox, QFontComboBox, QDialog)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt,QTimer
from PyQt5.QtGui import QTextCharFormat, QFont, QPixmap

import res_rc


from ui_MainWindow import Ui_MainWindow

class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QmyMainWindow,self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Theta Air Monitor")
        