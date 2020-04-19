from pynput import keyboard
from PyQt5 import QtCore

class KeyListener(QtCore.QObject):

    signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def on_press(self):
        self.signal.emit()

    def run(self):
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+h': self.on_press
        })
        self.listener.start()