from PyQt5.QtWidgets import QLabel


class UploadBubble(QLabel):

    def __init__(self, url):
        self.text = f'''
            <h3> Uploaded! </h3>
            <p> {url} </p>
        '''
