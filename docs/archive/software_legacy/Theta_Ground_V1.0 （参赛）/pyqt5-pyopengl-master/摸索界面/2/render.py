from PyQt5.QtGui import QColor, QOpenGLVersionProfile
from PyQt5.QtWidgets import QOpenGLWidget

# import OpenGL.GL as gl
# import OpenGL.GLU as glu
# import OpenGL.GLUT as glut

import numpy as np
from OpenGL import GL

class Render(QOpenGLWidget):#通过子例化，实现自定义
    
    def __init__(self, parent=None):
        super(Render, self).__init__(parent)

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