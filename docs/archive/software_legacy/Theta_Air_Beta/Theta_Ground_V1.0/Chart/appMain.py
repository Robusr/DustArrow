import sys
from PyQt5.QtWidgets import QApplication
from myMainWindow import QmyMainWindow

app = QApplication(sys.argv)
mainform = QmyMainWindow()
mainform.plot_test()
mainform.show()

sys.exit(app.exec_())

