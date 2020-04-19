from PyQt5.QtWidgets import QApplication
from windows import Window
from keylistener import KeyListener

import sys

def create_window():
    window = Window()
    return window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_window()
    app.exec_()