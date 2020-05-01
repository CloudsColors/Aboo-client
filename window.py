from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QDesktopWidget, QPushButton, QSystemTrayIcon, qApp
from PyQt5.QtGui import QIcon, QPixmap

from Modules.keylistener import KeyListener
from Modules.uploader import Uploader

from Components.canvaswindow import CanvasWindow
from Components.trayicon import TrayIcon
from Components.uploadbubble import UploadBubble
from Components.warningbubble import WarningBubble
from Components.settings import Settings

from datetime import datetime
import webbrowser, os, sys

class Window(QMainWindow):

    _SAVE_PATH_FILE = os.path.join(os.path.abspath("."), "temp", "temp_file.png")
    _SAVE_SETTINGS_FILE = os.path.join(os.path.abspath("."), "settings", "settings.json")
    _SHOW_TRAY_INFO_MSG_ONCE = True
    _APP_VERSION = "0.99:2020-04-26"

    def resource_path(self, relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def __init__(self, parent=None):
        self._PATH_CURRENT = self.resource_path(".")
        self._PATH_STATICS = self.resource_path("Statics")
        super(Window, self).__init__(parent)
        self.settings = Settings(self.resource_path(self._SAVE_SETTINGS_FILE), self)
        self.settings._SIGNAL_WARNING.connect(lambda msg: self.on_settings_warning(msg))
        self.title = "Aboo-client"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 800
        self.bubbles = list()
        self.init_window()
        self.init_key_listener()

    ''' --- Listeners --- '''

    def init_key_listener(self):
        self.settings.is_settings_init()
        _HOTKEY = self.settings._SETTINGS["screenshot_hotkey"]
        self.keyListener = KeyListener(_HOTKEY, self)
        res = self.keyListener.run()
        self.keyListener._SIGNAL.connect(self.on_hotkey_create_canvas)
        # If something went wrong initializing the keylistener
        if(res[0] == False):
            self.display_new_warning_bubble(res[1])

    def init_close_listener(self):
        for dialog in self.dialogs:
            dialog._SIGNAL_CANCEL.connect(self.on_close_canvases)
            dialog._SIGNAL_SUCCESS.connect(lambda file: self.on_screenshot_success(file))

    ''' --- Events --- '''

    def on_settings_warning(self, msg):
        self.display_new_warning_bubble(msg)

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
            self.dialog = CanvasWindow(screenGeometry.x(), screenGeometry.y(), self._SAVE_PATH_FILE, self)
            self.dialogs.append(self.dialog)
            self.dialog.showFullScreen()
            self.dialog.move(screenGeometry.x(), screenGeometry.y())
        self.init_close_listener()

    def on_tray_double_clicked(self, event):
        if(event == QSystemTrayIcon.DoubleClick):
            self.show()

    def on_screenshot_success(self, file):
        uploader = Uploader()
        res = uploader.upload_screenshot(file)
        if(res[0] == False):
            self.display_new_warning_bubble(res[1])
            return
        if(self.settings._SETTINGS["open_browser_after_upload"]):
            webbrowser.open(res[1])
        if(self.settings._SETTINGS["copy_to_clipboard_after_upload"]):
            qApp.clipboard().setText(res[1])
        if(self.settings._SETTINGS["open_notification_on_upload"]):
            self.trayIcon.showMessage(
                "Aboo-client",
                "Screenshot uploaded",
                QSystemTrayIcon.Information,
                2000
            )
        self.display_new_upload_bubble(True, file, res[1])

    def closeEvent(self, event):
        if(not self.settings._SETTINGS["system_tray_on_close"]):
            qApp.quit()
            return
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
        pixmap = QPixmap(self._PATH_STATICS+'/logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setGeometry(0, 0, 800, 200)
        self.logo.setStyleSheet("background-color: #81B1D5; border-bottom: 1px solid black")
        # Version label
        self.versionLabel = QLabel(self)
        self.versionLabel.setText("Version: "+self._APP_VERSION)
        self.versionLabel.setStyleSheet("color: black")
        self.versionLabel.setGeometry(630, 763, 200, 25)
        #Canvas windows list
        self.dialogs = list()
        #Settings button
        self.settingsButton = QPushButton("Settings", self)
        self.settingsButton.clicked.connect(self.settings.show_settings)
        self.settingsButton.setGeometry(20, 763, 80, 25)
        self.settingsButton.setStyleSheet("color: black; background-color: white")
        #Window settings
        qApp.setQuitOnLastWindowClosed(False) # Need this to not quit when canvasWindow is closed
        self.setStyleSheet("background-color: #81B1D5;")
        self.setWindowIcon(QIcon(self._PATH_STATICS+"/icon-large.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        #Tray settings
        self.trayIcon = TrayIcon(self.resource_path("Statics/icon-large.png"))
        self.trayIcon.activated.connect(self.on_tray_double_clicked)
        self.trayIcon.show()
        #Show the window
        self.show()

    ''' --- GUI Bubbles --- '''

    def display_new_upload_bubble(self, success, file, url="Failed to upload :("):
        if(len(self.bubbles) == 4):
            self.rearrange_bubbles()
        uploadBubble = UploadBubble(success, file, len(self.bubbles), url, self)
        uploadBubble.show()
        self.bubbles.append(uploadBubble)

    def display_new_warning_bubble(self, msg):
        if(len(self.bubbles) == 4):
            self.rearrange_bubbles()
        warningBubble = WarningBubble(len(self.bubbles), msg, self)
        warningBubble.show()
        self.bubbles.append(warningBubble)

    def rearrange_bubbles(self):
        bubbleToRemove = self.bubbles.pop(0)
        bubbleToRemove.close()
        for i in range(0, len(self.bubbles)):
            self.bubbles[i].move(15,215+(i*115))