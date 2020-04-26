from PyQt5.QtWidgets import QLabel

class WarningBubble(QLabel):

    _WIDTH = 390
    _HEIGHT = 100
    _PADDING = 15

    def __init__(self, nrOfBubbles, text, parent=None):
        super(WarningBubble, self).__init__(parent)
        self.text = text
        self.parent = parent
        self.nrOfBubbles = nrOfBubbles
        self.init_upload_bubble()

    def init_upload_bubble(self):
        self.setText(self.text)
        self.setWordWrap(True)
        self._UPLOADED = False
        self.setStyleSheet("background-color: rgba(255,255,0,85%); border: 1px solid #0F084B; border-radius: 5px;")
        self.setGeometry(15, 215 + (self.nrOfBubbles * (self._HEIGHT+self._PADDING)), self._WIDTH, self._HEIGHT)