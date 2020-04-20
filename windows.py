from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor
from PyQt5 import QtCore
from keylistener import KeyListener

class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.title = "Aboo-client"
        self.top = 100
        self.left = 100
        self. width = 800
        self.height = 600
        self.init_window()
        self.init_key_listener()

    def init_key_listener(self):
        self.keyListener = KeyListener()
        self.keyListener.run()
        self.keyListener.signal.connect(self.on_hotkey_create_canvas)

    def on_hotkey_create_canvas(self):
        self.dialog = CanvasWindow(self)
        self.dialogs.append(self.dialog)
        self.dialog.showFullScreen()
    
    def init_window(self):
        self.dialogs = list()
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

class CanvasWindow(QMainWindow):

    def __init__(self, parent=None):
        super(CanvasWindow, self).__init__()
        self.mousePressed = None
        self.mouseNow = None
        self.top = 0
        self.left = 0
        self.width = 1920
        self.height = 1080
        self.init_window()

    def keyPressEvent(self, e):
        if(e.key() == QtCore.Qt.Key_Escape):
            self.close()

    def mouseMoveEvent(self, e):
        self.mouseNow = e.pos()
        self.update()

    def mousePressEvent(self, e):
        self.mousePressed = e.pos()

    def mouseReleaseEvent(self, e):
        #todo: Make opacity 0.0
        #todo: take screenshot over area
        #todo: close the window
        return
    
    def init_window(self):
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowOpacity(0.9)
        #Remove titlebar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def paintEvent(self, event):
        if(self.mouseNow == None or self.mousePressed == None):
            return
        self.painter = QPainter(self)
        self.painter.setPen(QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        x1, y1, x2, y2 = self.mousePressed.x(), self.mousePressed.y(), self.mouseNow.x(), self.mouseNow.y()
        self.painter.drawRect(x1, y1, x2-x1, y2-y1)
        self.painter.end()