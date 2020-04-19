from PyQt5.QtWidgets import QMainWindow

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Aboo-client"
        self.top = 100
        self.left = 100
        self. width = 800
        self.height = 600
        self.init_window()
        self.keyPressEvent = self.on_key_pressed
    
    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def on_key_pressed(self, e):
        print("Key pressed: ",e.key())

