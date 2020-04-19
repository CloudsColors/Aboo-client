from PyQt5.QtWidgets import QMainWindow
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
        self.top = 0
        self.left = 0
        self.width = 1920
        self.height = 1080
        self.init_window()
    
    def init_window(self):
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowOpacity(0.7)
        #Remove titlebar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)