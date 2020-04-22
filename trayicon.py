from PyQt5.QtWidgets import QSystemTrayIcon, qApp, QMenu, QAction
from PyQt5.QtGui import QIcon

class TrayIcon(QSystemTrayIcon):

    def __init__(self):
        super().__init__()
        self.init_tray_icon()

    def init_tray_icon(self):
        self.setIcon(QIcon("statics/icon-small"))
        showAction = QAction("Show Aboo", self)
        quitAction = QAction("Exit", self)
        showAction.triggered.connect(self.show)
        quitAction.triggered.connect(qApp.quit)
        trayMenu = QMenu()
        trayMenu.addAction(showAction)
        trayMenu.addAction(quitAction)
        self.setContextMenu(trayMenu)
