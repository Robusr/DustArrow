from PyQt5 import QtWidgets
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class openGL_Widget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


    
        # 这个三个是虚函数, 需要重写
        # paintGL
        # initializeGL
        # resizeGL

    # 启动时会先调用 initializeGL, 再调用 resizeGL , 最后调用两次 paintGL
    # 出现窗口覆盖等情况时, 会自动调用 paintGL
    # 调用过程参考 https://segmentfault.com/a/1190000002403921
    # 绘图之前的设置
    def initializeGL(self):
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.01, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
        # 绘图函数
    def paintGL(self):
        glLoadIdentity()
        glTranslatef(0,0.5,-6)
        self.rTri = 45
        glRotatef(self.rTri,0.0,1.0,0.0)
        glRotatef(self.rTri,0.0,0.0,1.0)


        glBegin(GL_QUADS)

        #顶面
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)     #右上顶点
        glVertex3f(-1.0, 1.0, -1.0)   #左上顶点
        glVertex3f(-1.0, 1.0, 1.0)     #左下顶点
        glVertex3f(1.0, 1.0, 1.0)      #右下顶点

        #底面
        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(1.0, -1.0, 1.0)     #右上顶点
        glVertex3f(-1.0, -1.0, 1.0)    #左上顶点
        glVertex3f(-1.0, -1.0, -1.0)   #左下顶点
        glVertex3f(1.0, -1.0, -1.0)    #右下顶点

        #前面
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, 1.0)      #右上顶点
        glVertex3f(-1.0, 1.0, 1.0)     #左上顶点
        glVertex3f(-1.0, -1.0, 1.0)    #左下顶点
        glVertex3f(1.0, -1.0, 1.0)     #右下顶点

        #后面
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)   #右上顶点
        glVertex3f(-1.0, -1.0, -1.0)   #左上顶点
        glVertex3f(-1.0, 1.0, -1.0)    #左下顶点
        glVertex3f(1.0, 1.0, -1.0)     #右下顶点

        #左侧面
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)     #右上顶点
        glVertex3f(-1.0, 1.0, -1.0)    #左上顶点
        glVertex3f(-1.0, -1.0, -1.0)   #左下顶点
        glVertex3f(-1.0, -1.0, 1.0)    #右下顶点

        #右侧面
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)     #右上顶点
        glVertex3f(1.0, 1.0, 1.0)     #左上顶点
        glVertex3f(1.0, -1.0, 1.0)     #左下顶点
        glVertex3f(1.0, -1.0, -1.0)    #右下顶点

        glEnd()
        #绘制正方形结束

        

    