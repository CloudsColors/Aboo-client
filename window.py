from PyQt5.QtWidgets import QApplication, QLabel

class Window:

    def __init__(self, size, name):
        self.name = name
        self.size = size
        self.construct_window()
    
    def construct_window(self):
        app = QApplication([])
        label = QLabel("Hello world")
        label.show()
        app.exec_()
