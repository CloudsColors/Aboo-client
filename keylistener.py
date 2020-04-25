from pynput import keyboard
from PyQt5 import QtCore

class KeyListener(QtCore.QObject):

    _SIGNAL = QtCore.pyqtSignal()
    _HOTKEY = "<ctrl>+<alt>+s"

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        if(not self.parent == None and self.parent.settings._SETTINGS == True):
            self._HOTKEY = self.parent.settings.settings["screenshot_hotkey"]

    def on_press(self):
        self._SIGNAL.emit()

    def run(self):
        try:
            self.listener = keyboard.GlobalHotKeys({
                self._HOTKEY: self.on_press
            })
            self.listener.start()
        except:
            print("hotkey format is wrong, please fix in your settings and restart the application")