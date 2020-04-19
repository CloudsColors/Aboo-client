from PyQt5.QtWidgets import QApplication
from window import Window
from keylistener import start_listening

import sys

def create_window():
    keyboard_listener = start_listening()
    window = Window()
    return window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_window()
    app.exec_()