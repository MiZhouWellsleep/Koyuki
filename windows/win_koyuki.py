import sys

from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme,
                            NavigationAvatarWidget,  SplitFluentWindow, FluentTranslator, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from .subwin_koyuki.home_interface import HomeInterface
from .subwin_koyuki.ba_student_search import BaStudentSearchInterface
from .subwin_koyuki.ba_data import BaDataInterface

from .subwin_koyuki.CONFIG import COMMON_ICON

class WinKoyuki(FluentWindow):
    def __init__(self, parent):
        super().__init__()
        parent=parent
        self.initWindow()
        self.initSubwin()
        self.initNavigation()
        self.splashScreen.finish()
        
    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon('./img/1.png'))
        self.setWindowTitle('小雪功能面板')
        # create splash screen
        self.splashScreen = SplashScreen(QIcon(COMMON_ICON), self)
        self.splashScreen.setIconSize(QSize(400, 400))
        self.splashScreen.raise_()
        
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

        
    def initSubwin(self):
        self.home_interface = HomeInterface(self)
        self.baSearchInterface = BaStudentSearchInterface(self)
        self.baDataInterface = BaDataInterface(self)
        
    def initNavigation(self):
        self.addSubInterface(self.home_interface, FIF.HOME, self.tr('主页面'))
        self.addSubInterface(self.baSearchInterface, FIF.SEARCH, self.tr("碧蓝档案学生攻略查询"))
        self.addSubInterface(self.baDataInterface, FIF.DOCUMENT, self.tr('碧蓝档案国际服攻略'))
    
    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.splashScreen.resize(self.size())
        
