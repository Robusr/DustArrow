echo off
copy .\QtApp\mainwindow.ui mainwindow.ui
pyuic5 -o ui_MainWindow.py mainwindow.ui

pyrcc5 .\QtApp\res.qrc -o res_rc.py