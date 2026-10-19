from PyQt5.QtGui import QColor, QOpenGLVersionProfile
from PyQt5.QtWidgets import QOpenGLWidget

# import OpenGL.GL as gl
# import OpenGL.GLU as glu
# import OpenGL.GLUT as glut

import numpy as np
from OpenGL import GL

from PyQt5.QtCore import *

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
        version_profile = QOpenGLVersionProfile()
        version_profile.setVersion(2, 0)
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()
        
        #设置背景色
        self.gl.glClearColor(0.2, 0.4, 0.52, 1.0)
        # #深度测试
        # self.gl.glEnable(self.gl.GL_DEPTH_TEST)


        
    def paintGL(self):

        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)

        self.gl.glPushMatrix()
        self.gl.glTranslatef(self.dX,self.dY,0)
        self.gl.glScalef(self.scale,self.scale,1.0)
    
        self.gl.glColor3d(1.0, 0.0, 0.0)
        #VAO
        self.gl.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glVertexPointer(3,GL.GL_FLOAT,0,*(self.vertices))
        GL.glDrawArrays(GL.GL_LINES,0,len(self.vertices))#从第0个开始，访问X个

        #glut.glutWireTeapot(1)
        #glut.glutWireSphere(2, 13, 13)

        # #self.gl.glRotated(60.0, 1.0, 0.0, 0.0)       
        # self.gl.glBegin(self.gl.GL_TRIANGLES)
        # self.gl.glColor3d(1.0, 0.0, 0.0)
        # self.gl.glVertex3d(0.0, 1.0, 0.0)
        # self.gl.glColor3d(0.0, 1.0, 0.0)
        # self.gl.glVertex3d(-1.0, -1.0, 0.0)
        # self.gl.glColor3d(0.0, 0.0, 1.0)
        # self.gl.glVertex3d(1.0, -1.0, 0.0)
        # self.gl.glEnd()
 
        # self.gl.glBegin(self.gl.GL_LINES)
        # self.gl.glVertex3d(-1.5,-1.5,0)
        # self.gl.glVertex3d(1.5,1.5,0)
        # self.gl.glEnd()

        self.gl.glPopMatrix()
        
    def resizeGL(self, width, height):
 
        side = min(width, height)
        if side < 0:
            return
            
        #视口
        self.gl.glViewport((width - side) // 2, (height - side) // 2, side, side)
        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()
        #正交投射
        self.gl.glOrtho(-1.5, 1.5, -1.5, 1.5, -10, 10)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)


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
        #暂时用不到
        # elif event.button() == Qt.RightButton:
        #     # Render.dX+=0.3
        #     # self.update()
        #     print("鼠标右键点击")
        # elif event.button() == Qt.MidButton:
        #     print("鼠标中键点击")

    def mouseMoveEvent(self, event) -> None:
        # print(event.globalPos())#鼠标相对桌面的坐标
        # print(event.localPos())#鼠标相对控件的坐标
        self.end=event.localPos()
        self.dX+=(self.end.x()-self.begin.x())/200
        self.dY+=-(self.end.y()-self.begin.y())/200#原点在左上，OpenGL原点在左下，所以取反
        self.begin=self.end
        self.update()
        #print("moveEvent")

    