from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor, QPixmap
from PyQt5 import QtCore, Qt

class CanvasWindow(QMainWindow):

    _RIGHT_CLICK = 2
    _LEFT_CLICK = 1

    def __init__(self, parent=None):
        super(CanvasWindow, self).__init__()
        self.mP = None #Mouse position when pressed
        self.mN = None #Mouse position right now (to create the box drawing)
        self.mR = None #Mouse position when released
        self.init_window()

    def keyPressEvent(self, e):
        if(e.key() == QtCore.Qt.Key_Escape):
            self.close()

    def mouseMoveEvent(self, e):
        self.mN = e.pos()
        self.update()

    def mousePressEvent(self, e):
        if(e.button() == self._LEFT_CLICK):
            self.mP = e.pos()
        if(e.button() == self._RIGHT_CLICK):
            self.close_window()

    def mouseReleaseEvent(self, e):
        self.mR = e.pos()
        self.take_screenshot()
    
    def take_screenshot(self):
        self.setWindowOpacity(0.0)
        if(self.mP.x() < self.mR.x()):
            upperLeft = self.mP.x()
        else:
            upperLeft = self.mR.x()
        if(self.mP.y() < self.mR.y()):
            upperY = self.mP.y()
        else:
            upperY = self.mR.y()
        height = abs(self.mP.y() - self.mR.y())
        width = abs(self.mR.x() - self.mP.x())
        screen = QApplication.primaryScreen().grabWindow(0, upperLeft, upperY, width, height)
        screen.save("temp_file_name.png")
        self.close_window()

    def close_window(self):
        self.close()

    def init_window(self):
        self.setWindowOpacity(0.1)
        #Remove titlebar and make window stay on top
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    def paintEvent(self, event):
        if(self.mN == None or self.mP == None):
            return
        self.painter = QPainter(self)
        self.painter.setPen(QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        self.painter.drawRect(self.mP.x(), self.mP.y(), self.mN.x()-self.mP.x(), self.mN.y()-self.mP.y())
        self.painter.end()