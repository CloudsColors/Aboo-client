from PyQt5.QtWidgets import QMainWindow

import json, traceback

class Settings(QMainWindow):

    _SETTINGS = False
    
    def __init__(self):
        self.read_settings()

    def read_settings(self):
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
                self._SETTINGS = True
                f.close()
        except:
            self._SETTINGS = False
        
if __name__ == "__main__":
    settings = Settings()
    print(settings.settings["screenshot_hotkey"])
    