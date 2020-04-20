from PyQt5.QtWidgets import QMainWindow
from keylistener import KeyListener
from canvaswindow import CanvasWindow

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