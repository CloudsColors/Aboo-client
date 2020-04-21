from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QIcon
from keylistener import KeyListener
from canvaswindow import CanvasWindow

class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.title = "Aboo-client"
        self.top = 100
        self.left = 100
        self. width = 800
        self.height = 800
        self.init_window()
        self.init_key_listener()

    def init_key_listener(self):
        self.keyListener = KeyListener()
        self.keyListener.run()
        self.keyListener._SIGNAL.connect(self.on_hotkey_create_canvas)

    def init_close_listener(self):
        for dialog in self.dialogs:
            dialog._SIGNAL.connect(self.on_close_canvases)

    def on_close_canvases(self):
        for dialog in self.dialogs:
            dialog.close()
        self.dialogs.clear()

    def on_hotkey_create_canvas(self):
        #Clear any windows that already are open (to prevent several layers of windows)
        self.on_close_canvases()
        #Read in nr of monitors the user has
        nrOfScreens = QDesktopWidget().screenCount()
        #Loop through and start the canvas on each of the monitor.
        for i in range(0, nrOfScreens):
            screenGeometry = QDesktopWidget().availableGeometry(i)
            self.dialog = CanvasWindow(screenGeometry.x(), screenGeometry.y(), self)
            self.dialogs.append(self.dialog)
            self.dialog.showFullScreen()
            self.dialog.move(screenGeometry.x(), screenGeometry.y())
        self.init_close_listener()
    
    def init_window(self):
        #Logo
        self.logo = QLabel(self)
        pixmap = QPixmap('statics/logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setGeometry(0,0,800,200)
        self.logo.setStyleSheet("background-color: #3D60A7")
        #Canvas windows list
        self.dialogs = list()
        #Window settings
        self.setStyleSheet("background-color: #A0D2E7;")
        self.setWindowIcon(QIcon("statics/icon-medium.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        #Show the window
        self.create_new_upload_bubble()
        self.show()

    def create_new_upload_bubble(self):
        self.uploadText = QLabel(self)
        self.uploadText.setText("<h3> New entry </h3> \n <a href='https://www.aboo.se/'> Link </a> \n TTL: 2020-04-22 21:11")
        self.uploadText.setGeometry(5, 220, 390, 100)
        self.uploadText.setStyleSheet("background-color: #81B1D5; border: 1px solid black; border-radius: 5px")



    #todo: import webbrowser
    #todo: webbrowser.open(url)