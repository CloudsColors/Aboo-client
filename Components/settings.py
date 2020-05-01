from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

import json, traceback, os, sys

class Settings(QLabel):

    _SETTINGS = {"open_browser_after_upload": True, "copy_to_clipboard_after_upload": False, "open_notification_on_upload": False, "system_tray_on_close": True, "screenshot_hotkey": "<ctrl>+<alt>+s"}
    _SIGNAL_WARNING = pyqtSignal(str)
    _SETTINGS_READ = False
    
    def __init__(self, path, parent=None):
        super().__init__()
        self._PATH_SETTINGS_FILE = path
        self.parent = parent
        self.read_settings()
        self.init_gui()

    def read_settings(self):
        try:
            with open(self._PATH_SETTINGS_FILE, "r") as f:
                self._SETTINGS = json.load(f)
                f.close()
                self._SETTINGS_READ = True
        except:
            self.create_settings()

    def create_settings(self):
        try:
            os.mkdir("settings")
        except FileExistsError:
            pass
        with open(self._PATH_SETTINGS_FILE, "w") as f:
            f.write(json.dumps(self._SETTINGS))
            f.close()

    def is_settings_init(self):
        if(not self._SETTINGS_READ):
            self._SIGNAL_WARNING.emit("Error: settings was not read in properly. A new settings file has been created, if this was your first time launching the program then discard this message. Ctrl+Alt+s to screenshot is set as default")
        return


    def save_settings(self):
        self._SETTINGS["open_browser_after_upload"] = self.browser.isChecked()
        self._SETTINGS["copy_to_clipboard_after_upload"] = self.clipboard.isChecked()
        self._SETTINGS["open_notification_on_upload"] = self.notification.isChecked()
        self._SETTINGS["system_tray_on_close"] = self.tray.isChecked()
        self._SETTINGS["screenshot_hotkey"] = self.hotkey.text()
        try:
            with open(self._PATH_SETTINGS_FILE, "r+") as f:
                f.truncate(0)
                f.write(json.dumps(self._SETTINGS))
                f.close()
        except:
            self._SIGNAL_WARNING.emit("Error: Something went wrong and settings was not saved. Most likely settings.json was not found at the proper directory.")
        self.close()

    def show_settings(self):
        #move screen to where aboo-client is positioned right now
        self.move(self.parent.pos().x()+200, self.parent.pos().y()+200)
        self.show()

    def init_gui(self):
        #Window settings
        self.setGeometry(100,100,500,500)
        self.setWindowTitle("Aboo-client settings")
        #Checkbox browser
        self.browser = QCheckBox("Open browser after upload",self)
        self.browser.setChecked(self._SETTINGS["open_browser_after_upload"])
        self.browser.move(10,10)
        #Checkbox clipboard
        self.clipboard = QCheckBox("Copy to clipboard after upload",self)
        self.clipboard.setChecked(self._SETTINGS["copy_to_clipboard_after_upload"])
        self.clipboard.move(10,30)
        #notification bubble
        self.notification = QCheckBox("Open notification after screenshot has been uploaded",self)
        self.notification.setChecked(self._SETTINGS["open_notification_on_upload"])
        self.notification.move(10,50)
        #Checkbox tray
        self.tray = QCheckBox("System tray on close",self)
        self.tray.setChecked(self._SETTINGS["system_tray_on_close"])
        self.tray.move(10,70)
        #input field label
        self.hotkey_label = QLabel("Shortcut for screenshot (needs restart after applying)", self)
        self.hotkey_label.move(10, 110)
        #Input field hotkey
        self.hotkey = QLineEdit(self)
        self.hotkey.setText(self._SETTINGS["screenshot_hotkey"])
        self.hotkey.move(10, 130)
        #Input field description
        label_text_desc = "The shortcut needs to follow the syntax (In any order): <ctrl> for CTRL, <shift> for SHIFT, <alt> for ALT etc. Use + to add more buttons between each button. Regular letters like 's' or 'a' is just by themselves without any brackets. No spaces between (It wont work then)"
        self.hotkey_desc = QLabel(label_text_desc, self)
        self.hotkey_desc.setWordWrap(True)
        self.hotkey_desc.setGeometry(10, 160, 400, 100)
        #Save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.move(10,460)
        #Cancel button
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.move(400,460)