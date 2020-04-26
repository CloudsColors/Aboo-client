from pynput import keyboard
from PyQt5.QtCore import pyqtSignal, QObject

class KeyListener(QObject):

    _SIGNAL = pyqtSignal()
    _HOTKEY = "<ctrl>+<alt>+s"

    def __init__(self, setSettings, _HOTKEY, parent=None):
        super().__init__()
        self.parent = parent
        if(setSettings):
            self._HOTKEY = _HOTKEY

    def on_press(self):
        self._SIGNAL.emit()

    def run(self):
        try:
            self.listener = keyboard.GlobalHotKeys({
                self._HOTKEY: self.on_press
            })
            self.listener.start()
            return (True, "")
        except:
            return (False, "Error: Hotkey is formatted wrong from settings, please format it correct and restart the application for shortcut to work.")