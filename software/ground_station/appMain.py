import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from myMainWindow import QmyMainWindow


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


# A windowed PyInstaller build has no console, so sys.stdout/stderr are None.
# The application still calls print() in a few runtime paths (port open, serial
# receive, OpenGL mouse handler); redirect those to devnull so they do not
# raise AttributeError when reached.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")


app = QApplication(sys.argv)
icon = QIcon(resource_path("QtApp/images/rocket.ico"))
app.setWindowIcon(icon)
mainform = QmyMainWindow()

mainform.show()
sys.exit(app.exec_())


