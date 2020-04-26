from pynput import keyboard
from PyQt5 import QtCore

class KeyListener(QtCore.QObject):

    _SIGNAL = QtCore.pyqtSignal()
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
        except:
            pass