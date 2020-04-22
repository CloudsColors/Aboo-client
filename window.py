from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QDesktopWidget, QAction, QSystemTrayIcon, qApp, QMenu
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from keylistener import KeyListener
from canvaswindow import CanvasWindow
from uploader import Uploader
from datetime import datetime
from trayicon import TrayIcon

import webbrowser

class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.title = "Aboo-client"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 800
        self.uploadBubbles = list()
        self.init_window()
        self.init_key_listener()

    ''' --- Listeners --- '''

    def init_key_listener(self):
        self.keyListener = KeyListener()
        self.keyListener.run()
        self.keyListener._SIGNAL.connect(self.on_hotkey_create_canvas)

    def init_close_listener(self):
        for dialog in self.dialogs:
            dialog._SIGNAL_CANCEL.connect(self.on_close_canvases)
            dialog._SIGNAL_SUCCESS.connect(self.on_screenshot_success)

    ''' --- Events --- '''

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

    def on_tray_double_clicked(self, event):
        if(event == QSystemTrayIcon.DoubleClick):
            self.show()

    def on_screenshot_success(self):
        uploader = Uploader()
        res = uploader.upload_screenshot("temp_file_name.png")
        if(res[0] == False):
            self.display_new_upload_bubble(False)
            return
        self.display_new_upload_bubble(True, res[1])
        webbrowser.open(res[1])

    def closeEvent(self, event):
        self.trayIcon.showMessage(
            "Aboo-client",
            "Application was minimized to tray and is still running, left click and chose exit to close the application!",
            QSystemTrayIcon.Information,
            1000
        )

    ''' --- GUI and window properties --- '''

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
        qApp.setQuitOnLastWindowClosed(False) # Need this to not quit when canvasWindow is closed
        self.setStyleSheet("background-color: #A0D2E7;")
        self.setWindowIcon(QIcon("statics/icon-medium.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        #Tray settings
        self.trayIcon = TrayIcon()
        self.trayIcon.activated.connect(self.on_tray_double_clicked)
        self.trayIcon.show()
        #Show the window
        self.show()

    def display_new_upload_bubble(self, success, url="Failed to upload :("):
        if(len(self.uploadBubbles) == 4):
            self.uploadBubbles.pop(0)
            for i in range(0, len(self.uploadBubbles)):
                self.uploadBubbles[i].move(15,215+(i*75))
        timeNow = datetime.now()
        time = timeNow.strftime("%Y-%m-%d %H:%M:%S")
        uploadText = QLabel(self)
        if(success):
            uploadText.setText(f"<h4> Uploaded {time} </h4><p>{url}</p>")
        else:
            uploadText.setText(f"<h4> Woops, upload failed!</h4><p>{url}</p>")
        uploadText.setGeometry(15, 215 + (len(self.uploadBubbles * 75)), 390, 60)
        uploadText.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 5px") #bg color #81B1D5
        uploadText.show()
        self.uploadBubbles.append(uploadText)