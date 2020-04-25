from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton

import json, traceback

class Settings(QLabel):

    _SETTINGS = False
    
    
    def __init__(self):
        super().__init__()
        self.read_settings()
        self.init_gui()

    def read_settings(self):
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
                self._SETTINGS = True
                f.close()
        except:
            self._SETTINGS = False

    def save_settings(self):
        self.settings["open_browser_after_upload"] = self.browser.isChecked()
        self.settings["copy_to_clipboard_after_upload"] = self.clipboard.isChecked()
        self.settings["system_tray_on_close"] = self.tray.isChecked()
        self.settings["screenshot_hotkey"] = self.hotkey.text()
        try:
            with open("settings.json", "w") as f:
                f.write(json.dumps(self.settings))
                f.close()
        except:
            self._SETTINGS = False
        self.close()

    def init_gui(self):
        #Window settings
        self.setGeometry(100,100,400,400)
        self.setWindowTitle("Aboo-client settings")
        #Checkbox browser
        self.browser = QCheckBox("Open browser after upload",self)
        self.browser.setChecked(self.settings["open_browser_after_upload"])
        self.browser.move(10,10)
        #Checkbox clipboard
        self.clipboard = QCheckBox("Copy to clipboard after upload",self)
        self.clipboard.setChecked(self.settings["copy_to_clipboard_after_upload"])
        self.clipboard.move(10,30)
        #Checkbox tray
        self.tray = QCheckBox("System tray on close",self)
        self.tray.setChecked(self.settings["system_tray_on_close"])
        self.tray.move(10,50)
        #input field label
        self.hotkey_label = QLabel("Shortcut for screenshot (needs restart after applying)", self)
        self.hotkey_label.move(10, 90)
        #Input field hotkey
        self.hotkey = QLineEdit(self)
        self.hotkey.setText(self.settings["screenshot_hotkey"])
        self.hotkey.move(10, 110)
        #Input field description
        label_text_desc = "The shortcut needs to follow the syntax (In any order): <ctrl> for CTRL, <shift> for SHIFT, <alt> for ALT etc. Use + to add more buttons between each button. Regular letters like 's' or 'a' is just by themselves without any brackets."
        self.hotkey_desc = QLabel(label_text_desc, self)
        self.hotkey_desc.setWordWrap(True)
        self.hotkey_desc.setGeometry(10, 140, 380, 60)
        #Save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.move(10,360)
        #Cancel button
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.move(310,360)

if __name__ == "__main__":
    settings = Settings()
    print(settings.settings["screenshot_hotkey"])