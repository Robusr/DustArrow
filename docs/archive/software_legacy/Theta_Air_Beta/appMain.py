import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from myMainWindow import QmyMainWindow

app = QApplication(sys.argv)
icon = QIcon("QtApp/images/UAV.ico")
app.setWindowIcon(icon)
mainform = QmyMainWindow()

mainform.show()
sys.exit(app.exec_())

