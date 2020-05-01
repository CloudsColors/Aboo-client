from PyQt5.QtWidgets import QLabel, qApp
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

from datetime import datetime
import webbrowser 

class UploadBubble(QLabel):

    _WIDTH = 390
    _HEIGHT = 100
    _LEFT_CLICK = 1
    _PADDING = 15
    _UPLOADED = False

    def __init__(self, success, file, nrOfBubbles, url, parent=None):
        super(UploadBubble, self).__init__(parent)
        self.parent = parent
        self.success = success
        self.nrOfBubbles = nrOfBubbles
        self.url = url
        self.init_upload_bubble()
        self.display_preview_image(file)
        self.mouseReleaseEvent = self.on_label_click

    def init_upload_bubble(self):
        timeNow = datetime.now()
        time = timeNow.strftime("%Y-%m-%d %H:%M:%S")
        if(self.success):
            self.setText(f"<h4> Uploaded {time} </h4><p>{self.url}</p>")
            self._UPLOADED = True
            self.setStyleSheet("background-color: rgba(255,255,255,85%); border: 1px solid #0F084B; border-radius: 5px;")
        else:
            self.setText(f"<h4> Woops, upload failed!</h4><p>{self.url}</p>")
            self._UPLOADED = False
            self.setStyleSheet("background-color: rgba(255,255,0,85%); border: 1px solid #0F084B; border-radius: 5px;")
        self.setGeometry(15, 215 + (self.nrOfBubbles * (self._HEIGHT+self._PADDING)), self._WIDTH, self._HEIGHT)
    
    def on_label_click(self, e):
        if(e.button() == self._LEFT_CLICK and self._UPLOADED):
            webbrowser.open(self.url)

    def display_preview_image(self, file):
        self.preview = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(file)
        adjusted_pixmap = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.preview.setPixmap(adjusted_pixmap)
        self.preview.resize(60, 60)
        self.preview.setGeometry(300, 20, 60, 60)
        self.preview.setStyleSheet("border: 1px solid black;")
