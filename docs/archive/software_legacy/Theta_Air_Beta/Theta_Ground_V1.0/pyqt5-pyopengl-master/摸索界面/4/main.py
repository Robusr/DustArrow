import  sys
from Ui_main import Ui_MainWindow
#import second as u2
from PyQt5.QtWidgets import  *
from render import Render#从此，OpenGL只管画图，消息响应由pyqt正式接管


# class SecondWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super(SecondWindow, self).__init__(parent)
#         self.ui = u2.Ui_Form()
#         self.ui.setupUi(self)

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    def slot1(self):
        print("响应信号的槽函数")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    #win2 = SecondWindow()
    sys.exit(app.exec_())
