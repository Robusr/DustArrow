import sys
import serial
import serial.tools.list_ports


from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from ui_demo_a import Ui_Form

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

from PyQt5 import QtWidgets                     #包含构建界面的UI元素组件




class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):                         #开头都这么写
        super(Pyqt5_Serial, self).__init__()    #开头都这么写
        self.setupUi(self)                      #开头都这么写
        self.init()                             #调用下面的init函数
        self.setWindowTitle("Ucom v1.2")        #设置标题
        self.ser = serial.Serial()
        self.port_check()                       #串口检测
        self.setWindowIcon(QIcon(':/Ucom.ico'))   #设置图标

        # 接收数据和发送数据数目置零
        self.data_num_received = 0              #接收数据清零
        self.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0                #发送数据清零
        self.lineEdit_2.setText(str(self.data_num_sended))
        self.ReceNumForClear = 0                # 接收框的数据个数用于自动清除  放到初始化只会初始化一次

        # 设置选项卡的名称
        self.tabWidget.setTabText(0, '数据接收')
        self.tabWidget.setTabText(1, '波形显示')
        # index = self.tabWidget.currentIndex()     #可以读取选项卡的状态




        # 添加图像显示的画布
        self.static_canvas = FigureCanvas(Figure())                     # 画布、渲染器
        layout = QtWidgets.QVBoxLayout(self.groupBox)                   # 添加垂直布局类groupBox
        layout.addWidget(self.static_canvas)                            # 向布局groupBox_1中添加渲染器
        tool_bar = NavigationToolbar(self.static_canvas, self.groupBox)  # 生成画布相关联的工具栏
        layout.addWidget(tool_bar)                                      # 向布局groupBox_2中添加工具栏
        self._static_ax1 = self.static_canvas.figure.subplots(1, 1)     # 从渲染器中的画布figure中，获取子布，也就是Axes（1行1列）


    def init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)             # 单击 检测串口 按钮链接到port_check函数

        # 串口信息显示
        self.s1__box_2.currentTextChanged.connect(self.port_imf)    # 当前文本改变(串口选择) 链接到串口信息函数

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)            # 单击 打开串口 按钮链接到打开串口函数

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)          # 单击 关闭串口 按钮链接到关闭串口函数

        # 发送数据按钮
        self.s3__send_button.clicked.connect(self.data_send)        # 单击 发送 按钮链接到数据发送函数


        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        self.timer_send_cb.stateChanged.connect(self.data_send_timer)

        # 定时器接收数据
        self.tit = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)              # 串口中断是2ms进一次

        # 清除发送窗口
        self.s3__clear_button.clicked.connect(self.send_data_clear)     #单击 清除 按钮链接到清除显示函数(清除发送区)

        # 清除接收窗口
        self.s2__clear_button.clicked.connect(self.receive_data_clear)  #单击 清除 按钮链接到清除显示函数(清除接收区)

        # 打开文件
        self.s3__openfile_button.clicked.connect(self.openFile)         # 单击 打开文件

        self.timer1 = QTimer()                                          # 调用QT的定时器,用于波形显示


    # ------------------按下检测串口按钮
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}                                              #创建一个字典，字典是可变的容器
        port_list = list(serial.tools.list_ports.comports())            #list是序列，一串数据，可以追加数据
        self.s1__box_2.clear()                                          #s1__box_2为串口选择列表
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])                             #将检测到的串口放置到s1__box_2串口选择列表
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")

    # ------------------串口选择下拉框选择com口
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()                            #当前显示的com口
        if imf_s != "":
            self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])#state_label显示窗口显当前串口

    # -------------------打开串口
    def port_open(self):
        self.ser.port = self.s1__box_2.currentText()                    #串口选择框
        self.ser.baudrate = int(9600)           #波特率输入框
        self.ser.bytesize = int(8)           #数据位输入框
        self.ser.stopbits = int(1)           #停止位输入框
        self.ser.parity = "N"                 #校验位输入框
        try:
            self.ser.open()
        except:
	        QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
        self.timer.start(2)                                             #打开串口接收定时器，周期为2ms
        if self.ser.isOpen():                                           #打开串口按下，禁用打开按钮，启用关闭按钮
            self.open_button.setEnabled(False)                          #禁用打开按钮
            self.close_button.setEnabled(True)                          #启用关闭按钮
            self.formGroupBox1.setTitle("串口状态（已开启）")              #GroupBox1控件在串口打开的时候显示（已开启）

    # --------------------关闭串口
    def port_close(self):
        self.timer.stop()                                               # 停止计时器
        self.timer_send.stop()                                          # 停止定时发送
        self.timer1.stop()                                              # 停止图形显示计时器
        try:
            self.ser.close()
        except:
	        pass
        self.open_button.setEnabled(True)                               #启用打开按钮
        self.close_button.setEnabled(False)                             #禁用停止按钮
        self.lineEdit_3.setEnabled(True)                                #启用定时发送时间框
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.lineEdit.setText(str(self.data_num_received))              #接收数目置零
        self.data_num_sended = 0
        self.lineEdit_2.setText(str(self.data_num_sended))              #发送数目清零
        self.formGroupBox1.setTitle("串口状态（已关闭）")                  #GroupBox1控件在串口打开的时候显示（已关闭）

    # ----------------------发送数据
    def data_send(self):
        if self.ser.isOpen():                                           #判断串口是否打开 ↓
            input_s = self.s3__send_text.toPlainText()                  #（发送区）获取文本内容
            if input_s != "":                                           # 非空字符串 ↓
                # hex发送
                if self.hex_send.isChecked():                           #(勾选Hex发送) ↓（复选框选中返回Ture）
                    input_s = input_s.strip()                           #移除字符串头尾指定的字符（默认为空格或换行符）
                    send_list = []                                      #创建一个列表
                    while input_s != '':                                #发送框不是空的说明有数据，等发送完毕跳出循环
                        try:                                            #捕获异常
                            num = int(input_s[0:2], 16)                 #十六进制(取前两个字节数据)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()                   #移除字符串头尾指定的字符（默认为空格或换行符）
                        send_list.append(num)                           #列表末尾添加新的对象
                    input_s = bytes(send_list)                          #返回字节对象
                # ascii发送
                else:
                    input_s = (input_s + '\r\n').encode('utf-8')        #

                num = self.ser.write(input_s)                           #串口写，返回的写入的数据数
                self.data_num_sended += num                             #发送数据统计
                self.lineEdit_2.setText(str(self.data_num_sended))      #已发送数据显示框
        else:
	        pass #空语句 保证结构的完整性

    # ----------------------接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()                                  # 获取接受缓存中的字符数
        except:
            self.port_close()
            return None

        if num > 0:                                                     # 如果收到数据 数据以十六进制的形式放到data里面     ,接收一次数据进一次（也就是发送端点一次发送进一次）
            data = self.ser.read(num)                                   # 从串口读取指定字节大小的数据
            num = len(data)                                             # 等到收到数据的长度
            self.recevive_num = num
            # hex显示
            if self.hex_receive.checkState():                           # 如果勾选HEX接收
                out_s = ''                                              # 如果是空的，显示空格
                self.display = []                                       # 创建一个列表,用于暂存波形波形显示
                self.display2 = []                                      # 创建一个列表,用于图形绘制
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '      # 字符串操作显示到接收框(格式为2位十六进制)
                    self.display.append(data[i])
                self.s2__receive_text.insertPlainText(out_s)            # 接收的数据显示至接收区

                # 调用定时器实现图形绘制
                self.timer1.start(100)  # 单位为ms，10ms刷新一次

                self.i = 0  # 新建变量
                self.t = []  # 新建一个列表
                self.s = []  # 新建一个列表

                self.timer1.timeout.connect(self.refresh_plot)  # 定时器计数达到后调用函数refresh_plot


            # 如果不勾选HEX接收
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                self.s2__receive_text.insertPlainText(data.decode('iso-8859-1'))    #接收区

            # 统计接收字符的数量
            self.data_num_received += num                               # 更新接收到所有数据的数目
            self.ReceNumForClear += num                                 # 更新接收框里面的数据的数据
            self.lineEdit.setText(str(self.data_num_received))          # 显示接收数据个数
            if self.SetAutoClear.checkState():                          # 如果勾选自动清除
                ValueClearNumSet = int(self.ClearNumSet.text())         # 获取设定的自动清除的num值
                if self.ReceNumForClear >= ValueClearNumSet:            # 如果收到的数据大于等于ValueClearNumSet 有缺陷必须是等于才会清掉
                    self.s2__receive_text.setText("")                   # 清楚接收框 不清计数
                    self.ReceNumForClear = 0                            # ReceNumForClear清零用于下一次统计接收框接收数据个数
                    self.ReceNumForClear = self.ReceNumForClear         # 调试用

            # 获取到text光标
            textCursor = self.s2__receive_text.textCursor()             #获取接收区光标
            # 滚动到底部
            textCursor.movePosition(textCursor.End)                     #
            # 设置光标到text中去
            self.s2__receive_text.setTextCursor(textCursor)
        else:
            pass


    # -------------------------接收定时器达到时被调用
    def refresh_plot(self):                                             # 定时器数值达到时被调用
                                                             #
        if(self.i == self.recevive_num):                                # 画完图后关闭定时器
            self.timer1.stop()

        else:
            self.t.append(self.i)                                           # 列表后面添加i,生成横坐标
            self.display2.append(self.display[self.i])                      # 生成纵坐标
            self._static_ax1.cla()                                          # 清空子图
            self._static_ax1.plot(self.t, self.display2)                    # 绘制新的图
            self.static_canvas.draw()                                       # 更新字画布的渲染器
            self.i += 1

    # -------------------------定时发送数据
    def data_send_timer(self):
        if self.timer_send_cb.isChecked():                              # 勾选定时发送
            self.timer_send.start(int(self.lineEdit_3.text()))          # 勾选定时发送  lineEdit_3为定时时间（设置定时周期）
            self.lineEdit_3.setEnabled(False)                           # 禁用时间输入框
        else:
            self.timer_send.stop()                                      # 不勾选定时发送时，将发送定时器关闭
            self.lineEdit_3.setEnabled(True)                            # 不勾选定时发送时，使能时间输入框

    # ------------------------清除发送
    def send_data_clear(self):
        self.s3__send_text.setText("")                                  # 发送区
        self.data_num_sended = 0                                        # 清除的时候发送计数归零
        self.lineEdit_2.setText(str(self.data_num_sended))              # 已发送计数清零
    #  ------------------------清除接收
    def receive_data_clear(self):
        self.data_num_received = 0                                      # 清除的时候接收计数归零
        self.lineEdit.setText(str(self.data_num_received))              # 定时发送时间清除
        self.s2__receive_text.setText("")                               # 接收区清零



    # ------------------------打开文件
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')      # 打开文件
        if fname[0]:                                                    # fname[0]就是要打开的文件
            with open(fname[0], 'r', encoding='gb18030', errors='ignore') as f:
                self.s3__send_text.setText(f.read())                    # 将读取的文件放到发送框里面


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()     #调用class
    myshow.show()
    sys.exit(app.exec_())


