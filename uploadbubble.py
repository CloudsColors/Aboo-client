from PyQt5.QtWidgets import QLabel

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

    def init_upload_bubble(self):
        timeNow = datetime.now()
        time = timeNow.strftime("%Y-%m-%d %H:%M:%S")
        if(self.success):
            self.setText(f"<h4> Uploaded {time} </h4><p>{self.url}</p>")
        else:
            self.setText(f"<h4> Woops, upload failed!</h4><p>{self.url}</p>")
        self.setStyleSheet("background-color: rgba(255,255,255,85%); border: 1px solid #0F084B; border-radius: 5px;")
        self.setGeometry(15, 215 + (self.nrOfBubbles * (self._HEIGHT+10)), self._WIDTH, self._HEIGHT)
