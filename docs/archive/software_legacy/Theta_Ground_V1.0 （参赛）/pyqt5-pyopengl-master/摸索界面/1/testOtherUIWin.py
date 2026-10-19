import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QOpenGLWidget,QMessageBox
from PyQt5.uic import loadUi
from render import *#OpenGL窗口仅提供绘制功能，键盘鼠标响应由pyqt负责

class MainWin(QMainWindow):
    def __init__(self):
        #super().__init__()#super()构造器方法返回父级的对象。
        super(MainWin, self).__init__()
        self.ui=loadUi("MainWinWid.ui")#加载ui

        #绑定槽函数
        self.ui.pushButton_2.clicked.connect(self.test0)   

    def test0(self):
        print("槽函数响应")

app = QApplication(sys.argv)
w = MainWin()
w.ui.show()
sys.exit(app.exec())