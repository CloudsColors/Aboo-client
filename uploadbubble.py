from PyQt5.QtWidgets import QLabel

from datetime import datetime

class UploadBubble(QLabel):

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
        self.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 5px") #bg color #81B1D5
        self.setGeometry(15, 215 + (self.nrOfBubbles * 75), 390, 60)
