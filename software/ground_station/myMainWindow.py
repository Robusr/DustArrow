import sys
import time

from PyQt5 import QtCore,QtOpenGL
from PyQt5.QtWidgets import (QApplication, QMainWindow, QActionGroup, QLabel, QProgressBar,QMessageBox,
                             QSpinBox, QFontComboBox, QDialog)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt,QTimer
from PyQt5.QtGui import QTextCharFormat, QFont, QPixmap

import res_rc

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


import serial
import serial.tools.list_ports
import re
from opengl_widget import opengl_widget

from ui_MainWindow import Ui_MainWindow

class QmyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QmyMainWindow,self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("DustArrow Ground Monitor")
        self.ser = serial.Serial()
        self.port_check()
        #self.ddd = opengl_widget()

        self.tit = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.DATA) 
        
        

        self.timer1 = QTimer() 

        self.ui.pushButton_begin.clicked.connect(self.port_open)
        self.ui.pushButton_stop.clicked.connect(self.port_close)
        self.ui.comboBox_com.currentTextChanged.connect(self.port_imf)
        
        self.timer1 = QTimer()           

        self.figure_H = plt.figure() # 新建绘图区域H
        self.canvas_H  = FigureCanvasQTAgg(self.figure_H) # 绘图区域放到图层canvas之中
        self.ui.gridLayout_H.addWidget(self.canvas_H, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        self.figure_T_draw = self.canvas_H.figure.subplots(1, 1) 
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)

        self.figure_Pa = plt.figure() # 新建绘图区域Pa
        self.canvas_Pa = FigureCanvasQTAgg(self.figure_Pa ) # 绘图区域放到图层canvas之中
        self.ui.gridLayout_Pa.addWidget(self.canvas_Pa, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)

        self.figure_T = plt.figure() # 新建绘图区域T
        self.canvas_T = FigureCanvasQTAgg(self.figure_T) # 绘图区域放到图层canvas之中
        self.ui.gridLayout_T.addWidget(self.canvas_T, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)

        self.figure_W = plt.figure() # 新建绘图区域W
        self.canvas_W = FigureCanvasQTAgg(self.figure_W) # 绘图区域放到图层canvas之中
        self.ui.gridLayout_W.addWidget(self.canvas_W, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)

        self.figure_L = plt.figure() # 新建绘图区域L
        self.canvas_L = FigureCanvasQTAgg(self.figure_L) # 绘图区域放到图层canvas之中
        self.ui.gridLayout_L.addWidget(self.canvas_L, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)

        self.figure_6 = plt.figure() # 新建绘图区域PM
        self.canvas_6 = FigureCanvasQTAgg(self.figure_6) # 绘图区域放到图层canvas之中
        self.ui.gridLayout_6.addWidget(self.canvas_6, 0, 2, 2, 1) # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)

    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}                                              #创建一个字典，字典是可变的容器
        port_list = list(serial.tools.list_ports.comports())            #list是序列，一串数据，可以追加数据
        self.ui.comboBox_com.clear()                                          #s1__box_2为串口选择列表
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.ui.comboBox_com.addItem(port[0])                             #将检测到的串口放置到s1__box_2串口选择列表
        if len(self.Com_Dict) == 0:
           pass

    # ------------------串口选择下拉框选择com口
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.ui.comboBox_com.currentText()                            #当前显示的com口
        if imf_s != "":
            self.ui.plainTextEdit_message.setPlainText(self.Com_Dict[self.ui.comboBox_com.currentText()])

    # -------------------打开串口
    def port_open(self):
        self.ser.port = self.ui.comboBox_com.currentText()
        print(self.ui.comboBox_com.currentText() )                    #串口选择框
        self.ser.baudrate = int(9600)           #波特率输入框
        self.ser.bytesize = int(8)           #数据位输入框
        self.ser.stopbits = int(1)           #停止位输入框
        self.ser.parity = "N" #校验位输入框
        try:
            self.ser.open()
        except:
	        QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
        self.timer.start(5) 
        if self.ser.isOpen():                                           #打开串口按下，禁用打开按钮，启用关闭按钮
            self.ui.pushButton_begin.setEnabled(False)                          #禁用打开按钮                    
            self.ui.plainTextEdit_message.setPlainText("串口状态（已开启）") 
    def port_close(self):
        self.timer.stop()                                               # 停止计时器                                       
        self.timer1.stop()                                              # 停止图形显示计时器
        try:
            self.ser.close()
        except:
	        pass
        self.ui.pushButton_begin.setEnabled(True)
        self.ui.plainTextEdit_message.setPlainText("串口已关闭") 
        

    def DATA(self):
        try:
            num = self.ser.inWaiting()                                  # 获取接受缓存中的字符数
        except:
            self.port_close()
            return None

        if num > 0:                                                    
            data = self.ser.read(num)                                   
            num = len(data)                                             
            self.recevive_num = num
            self.ui.plainTextEdit_message.insertPlainText(data.decode('iso-8859-1'))
            print(data.decode('iso-8859-1'))
            #self.wb = xw.Book(r'data.xlsx')

            self.dataRead = data.decode('iso-8859-1')

            r = r"X(.+)Y(.+)GX(.+)GY(.+)GZ(.+)"
            m = re.findall(r,self.dataRead)
            for i in m:
                self.Gyrox = i[0]
                self.Gyroy = i[1]
                self.Gx = i[2]
                self.Gy = i[3]
                self.Gz = i[4]
 
            #self.ui.lcd_X.display(self.Gyrox)
            #self.ui.lcd_Y.display(self.Gyroy)
            with open("data.txt","w") as f:
                f.write("X"+self.Gyrox+"Y"+self.Gyroy) 
            #self.ui.widget.paintCube(self.Gyrox,self.Gyroy)



        

        

    