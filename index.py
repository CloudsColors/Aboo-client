from PyQt5.QtWidgets import QApplication
from window import Window

import sys

def create_window():
    window = Window()
    return window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_window()
    sys.exit(app.exec_())