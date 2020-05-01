from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QByteArray, QBuffer, QIODevice

import os

class CanvasWindow(QMainWindow):

    _RIGHT_CLICK = 2
    _LEFT_CLICK = 1
    _SIGNAL_CANCEL = pyqtSignal()
    _SIGNAL_SUCCESS = pyqtSignal(bytes)

    def __init__(self, xOffset, yOffset, path, parent=None):
        super(CanvasWindow, self).__init__()
        self._SAVE_PATH = path
        #Screen offset is used to calculate where the screenshot is taken when not on primary
        self.xOffset = xOffset
        self.yOffset = yOffset
        #Mouse coordinates is needed for when dragging out the rect where you want to screenshot
        self.mP = None #Mouse position when pressed
        self.mN = None #Mouse position right now (to create the box drawing)
        self.mR = None #Mouse position when released
        self.init_window()

    def keyPressEvent(self, e):
        if(e.key() == Qt.Key_Escape):
            self.close()

    def mouseMoveEvent(self, e):
        self.mN = e.pos()
        self.update()

    def mousePressEvent(self, e):
        if(e.button() == self._LEFT_CLICK):
            self.mP = e.pos()
        if(e.button() == self._RIGHT_CLICK):
            self._SIGNAL_CANCEL.emit()

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
        screen = QApplication.primaryScreen().grabWindow(0, upperLeft+self.xOffset, upperY+self.yOffset, width, height)
        rawFile = QByteArray()
        buff = QBuffer(rawFile)
        buff.open(QIODevice.WriteOnly)
        status = screen.save(buff, "PNG")
        if(not status):
            #todo add fail message
            self._SIGNAL_CANCEL.emit()
            return
        file = rawFile.data()
        self._SIGNAL_CANCEL.emit()
        self._SIGNAL_SUCCESS.emit(file)

    def close_window(self):
        self.close()

    def init_window(self):
        self.setWindowOpacity(0.2)
        #Remove titlebar and make window stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def paintEvent(self, event):
        if(self.mN == None or self.mP == None):
            return
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.painter.setOpacity(0.99)
        self.painter.drawRect(self.mP.x(), self.mP.y(), self.mN.x()-self.mP.x(), self.mN.y()-self.mP.y())
        self.painter.end()