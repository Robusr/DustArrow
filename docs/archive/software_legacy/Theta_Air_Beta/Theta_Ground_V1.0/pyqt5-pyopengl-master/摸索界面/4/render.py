from PyQt5.QtWidgets import QOpenGLWidget

import numpy as np

from PyQt5.QtCore import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Render(QOpenGLWidget):#通过子例化，实现自定义
    
    def __init__(self, parent=None):
        super(Render, self).__init__(parent)

        self.dX,self.dY=0,0#位移
        self.scale=1.0#缩放

        self.begin,self.end=QPoint(),QPoint()#用来获取鼠标的位置差

        #顶点数据
        self.vertices = np.array(
    [
        [-1, -1, 0], [0, 0, 0],
        [0, -1, 0],[1,1,0],
        [0,0,0],[0,1,0]
    ], dtype=np.float32



)  # define vertices
    def initializeGL(self):        
        #设置背景色
        glClearColor(0.2, 0.4, 0.52, 1.0)
        # #深度测试
        # self.gl.glEnable(self.gl.GL_DEPTH_TEST)



    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()
        glTranslatef(self.dX,self.dY,0)
        glScalef(self.scale,self.scale,1.0)
    
        glColor3d(1.0, 0.0, 0.0)
        #VAO
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3,GL_FLOAT,0,*(self.vertices))
        glDrawArrays(GL_LINES,0,len(self.vertices))#从第0个开始，访问X个

        glPopMatrix()
        
    def resizeGL(self, width, height):
 
        side = min(width, height)
        if side < 0:
            return
            
        #视口
        glViewport((width - side) // 2, (height - side) // 2, side, side)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #正交投射
        glOrtho(-1.5, 1.5, -1.5, 1.5, -10, 10)
        glMatrixMode(GL_MODELVIEW)


    #鼠标滚轮缩放
    def wheelEvent(self, event):
        angle=event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX=angle.x()  # 水平滚过的距离(此处用不上)
        angleY=angle.y()  # 竖直滚过的距离
        if angleY > 0:#滚轮上滚
            self.scale+=0.1
            self.update()
            print("鼠标滚轮上滚",angleY)  
        else:# 滚轮下滚
            self.scale-=0.1
            self.update()
            print("鼠标滚轮下滚",angleY)  


    #响应鼠标事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin=event.localPos()
            print("鼠标左键按下")

    def mouseMoveEvent(self, event) -> None:
        # print(event.globalPos())#鼠标相对桌面的坐标
        # print(event.localPos())#鼠标相对控件的坐标
        self.end=event.localPos()
        self.dX+=(self.end.x()-self.begin.x())/200
        self.dY+=-(self.end.y()-self.begin.y())/200#原点在左上，OpenGL原点在左下，所以取反
        self.begin=self.end
        self.update()
        #print("moveEvent")

    