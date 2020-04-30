from PyQt5.QtWidgets import QSystemTrayIcon, qApp, QMenu, QAction
from PyQt5.QtGui import QIcon

import os

class TrayIcon(QSystemTrayIcon):

    def __init__(self, path):
        super().__init__()
        self._PATH_STATICS = path
        self.init_tray_icon()

    def init_tray_icon(self):
        self.setIcon(QIcon(self._PATH_STATICS))
        showAction = QAction("Show Aboo", self)
        quitAction = QAction("Exit", self)
        showAction.triggered.connect(self.show)
        quitAction.triggered.connect(qApp.quit)
        trayMenu = QMenu()
        trayMenu.addAction(showAction)
        trayMenu.addAction(quitAction)
        self.setContextMenu(trayMenu)
