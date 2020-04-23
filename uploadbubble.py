from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

from datetime import datetime

class UploadBubble(QLabel):

    _WIDTH = 390
    _HEIGHT = 100

    def __init__(self, success, nrOfBubbles, url, parent=None):
        super(UploadBubble, self).__init__(parent)
        self.success = success
        self.nrOfBubbles = nrOfBubbles
        self.url = url
        self.init_upload_bubble()
        self.display_preview_image()

    def init_upload_bubble(self):
        timeNow = datetime.now()
        time = timeNow.strftime("%Y-%m-%d %H:%M:%S")
        if(self.success):
            self.setText(f"<h4> Uploaded {time} </h4><p>{self.url}</p>")
        else:
            self.setText(f"<h4> Woops, upload failed!</h4><p>{self.url}</p>")
        self.setStyleSheet("background-color: rgba(255,255,255,85%); border: 1px solid #0F084B; border-radius: 5px;")
        self.setGeometry(15, 215 + (self.nrOfBubbles * (self._HEIGHT+10)), self._WIDTH, self._HEIGHT)
    
    def display_preview_image(self):
        self.preview = QLabel(self)
        pixmap = QPixmap('temp_file_name.png')
        adjusted_pixmap = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.preview.setPixmap(adjusted_pixmap)
        self.preview.resize(60, 60)
        self.preview.setGeometry(300, 20, 60, 60)
        self.preview.setStyleSheet("border: 1px solid black;")
