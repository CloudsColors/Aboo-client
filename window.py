from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QDesktopWidget, QPushButton, QSystemTrayIcon, qApp
from PyQt5.QtGui import QIcon, QPixmap

from keylistener import KeyListener
from canvaswindow import CanvasWindow
from uploader import Uploader
from datetime import datetime
from trayicon import TrayIcon
from uploadbubble import UploadBubble

import webbrowser

class Window(QMainWindow):

    _SHOW_TRAY_INFO_MSG_ONCE = True
    _APP_VERSION = "0.9:2020-04-23"

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
        webbrowser.open(res[1])
        self.display_new_upload_bubble(True, res[1])

    def closeEvent(self, event):
        if(self._SHOW_TRAY_INFO_MSG_ONCE == False):
            return
        self.trayIcon.showMessage(
            "Aboo-client",
            "Application was minimized to tray and is still running, left click and chose exit to close the application!",
            QSystemTrayIcon.Information,
            2000
        )
        self._SHOW_TRAY_INFO_MSG_ONCE = False

    ''' --- GUI and window properties --- '''

    def init_window(self):
        #Background image
        self.label = QLabel(self)
        self.label.setGeometry(0, 200, 800, 550)
        self.label.setStyleSheet("background-color: #DFFFFF; border-bottom: 1px solid black")
        #Logo
        self.logo = QLabel(self)
        pixmap = QPixmap('statics/logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setGeometry(0, 0, 800, 200)
        self.logo.setStyleSheet("background-color: #81B1D5; border-bottom: 1px solid black")
        # Version label
        self.versionLabel = QLabel(self)
        self.versionLabel.setText("Version: "+self._APP_VERSION)
        self.versionLabel.setStyleSheet("color: black")
        self.versionLabel.setGeometry(650, 763, 200, 25)
        #Canvas windows list
        self.dialogs = list()
        #Settings button
        self.settingsButton = QPushButton("Settings", self)
        self.settingsButton.setGeometry(20, 763, 80, 25)
        self.settingsButton.setStyleSheet("color: black; background-color: white")
        #Window settings
        qApp.setQuitOnLastWindowClosed(False) # Need this to not quit when canvasWindow is closed
        self.setStyleSheet("background-color: #81B1D5;")
        self.setWindowIcon(QIcon("statics/icon-large.png"))
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
                self.uploadBubbles[i].move(15,215+(i*115))
        uploadBubble = UploadBubble(success, len(self.uploadBubbles), url, self)
        uploadBubble.show()
        self.uploadBubbles.append(uploadBubble)