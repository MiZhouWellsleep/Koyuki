from typing import List
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, LargeTitleLabel,ImageLabel, VBoxLayout, line_edit)
from .CONFIG import current_path
from .koyuki_interface import KoyukiInterface
from ..common.translator import Translator
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.trie import Trie

import requests
from io import BytesIO
from PIL import Image

from .CONFIG import COMMON_LOADING, COMMON_ERROR

class LineEdit(SearchLineEdit):
    """ 搜索框的LineEdit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('输入查找学生名称'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)
        
class FetchImageThread(QThread):
    imageFetched = pyqtSignal(QPixmap)
    fetchingStarted = pyqtSignal()
    fetchingFinished = pyqtSignal()

    def __init__(self, res_url):
        super().__init__()
        self.res_url = res_url

    def run(self):
        self.fetchingStarted.emit()
        try:
            response_img = requests.get(self.res_url)
            image_data = response_img.content
            image = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(image)
        except:
            pixmap = QPixmap(COMMON_ERROR)
        self.imageFetched.emit(pixmap)
        self.fetchingFinished.emit()

class StudentWikiView(QWidget):
    """ ba学生查询 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.trie = Trie()
        self.fetch_thread = None
        self.pixmap = None
        
        self.testLabel = StrongBodyLabel(self.tr('输入学生名称，查询学生攻略（支持部分别名搜索）'), self)
        self.searchLineEdit = LineEdit(self)
        self.resLabel = BodyLabel(self.tr('搜索结果在此处显示'), self)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        
        self.studentImg = ImageLabel(f"{current_path}/img/win_koyuki/banner/bilibili.jpg", self)
        self.studentImg.scaledToWidth(800)
        self.studentImg.setBorderRadius(8, 8, 8, 8)
        self.scrollArea.horizontalScrollBar().setValue(0)
        self.scrollArea.setWidget(self.studentImg)
        self.scrollArea.setFixedSize(800, 550)
        
        self.scrollWidget = QWidget(self.scrollArea)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=True)
        
        self.__initWidget()
        
    def __initWidget(self):
        #self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setViewportMargins(0, 15, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.addWidget(self.testLabel)
        self.vBoxLayout.addWidget(self.searchLineEdit)
        self.vBoxLayout.addWidget(self.resLabel)
        self.vBoxLayout.addWidget(self.view)
        
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        
        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)
        #self.searchLineEdit.clearSignal.connect(self.showAllIcons)
        self.searchLineEdit.searchSignal.connect(self.search)
        self.searchLineEdit.searchButton.clicked.connect(self.startSearch)
        
    def __setQss(self):
        self.view.setObjectName('iconView')
        self.scrollWidget.setObjectName('scrollWidget')

        StyleSheet.ICON_INTERFACE.apply(self)
        StyleSheet.ICON_INTERFACE.apply(self.scrollWidget)

        # if self.currentIndex >= 0:
        #     self.cards[self.currentIndex].setSelected(True, True)
        
    def search(self, keyWord: str):
        """ search icons """
        items = self.trie.items(keyWord.lower())
        indexes = {i[1] for i in items}
        self.flowLayout.removeAllWidgets()
        #print("*********\n")
        
    def startSearch(self):
        """ 按下按钮后开始查询ba学生攻略 """
        self.showStudentImg(QPixmap(COMMON_LOADING))    # loading图
        self.searchLineEdit.searchButton.setEnabled(False) # 禁用查询按钮
        name = self.searchLineEdit.text()
        url_babot = "https://raw.githubusercontent.com/lgc-NB2Dev/bawiki-data/main/data/stu_alias.json"
        url_arona = "https://raw.githubusercontent.com/diyigemt/arona/2.0.0-dev/tools/config/local_file_map.json"
        res = 'error'
        try:
            response_babot = requests.get(url_babot, verify=False)
            response_arona = requests.get(url_arona, verify=False)
            data_babot = response_babot.json()
            data_arona = response_arona.json()
            #res = "error"
            self.res_url = 'https://arona.cdn.diyigemt.com/image/student_rank/'
            for key, value in data_babot.items():
                if (name in value) or (name == key):
                    res = key
                    if data_babot[key][0] in data_arona.keys():
                        res = data_arona[data_babot[key][0]]
                    else:
                        res = res + '.png'
        except:
            res = 'error'
        if res == "error":
            self.resLabel.setText("出现问题！请检查输入是否有误，是否关闭网络代理")
            self.showStudentImg(QPixmap(COMMON_ERROR), isData=False)
            self.searchLineEdit.searchButton.setEnabled(True)   # 启用查询按钮
            return
        else:
            self.res_url = self.res_url + res
            self.fetch_image(self.res_url)
            self.resLabel.setText(self.res_url)
    
    def fetch_image(self, imgUrl):
        if self.fetch_thread is not None:
            self.fetch_thread.quit()
            self.fetch_thread.wait()
        self.fetch_thread = FetchImageThread(imgUrl)
        self.fetch_thread.imageFetched.connect(self.showStudentImg)
        self.fetch_thread.fetchingStarted.connect(self.fetching_start)
        self.fetch_thread.fetchingFinished.connect(self.fetching_finish)
        self.fetch_thread.start()
    
    def showStudentImg(self, pixmap, isData=True):
        """ 展示ba学生攻略图片 """
        self.pixmap = pixmap
        #self.studentImg.setPixmap(self.pixmap)
        self.adjustImgWidth()
        if isData:
            self.searchLineEdit.searchButton.setEnabled(True)
    
    def fetching_start(self):
        self.resLabel.setText("开始查询......")
    
    def fetching_finish(self):
        self.resLabel.setText(f"查询完成，图片来源{self.res_url}")
        
    def _adjustImgWidth(self):
        if self.pixmap is not None:
            size = self.width() - 200
            if size > 1000:
                size = 1000
            pixmap = self.pixmap.scaledToWidth(size, Qt.SmoothTransformation)
            self.studentImg.setPixmap(pixmap)
    def adjustImgWidth(self):
        self.studentImg.setPixmap(self.pixmap)
        self.studentImg.scaledToWidth(800)
            
        
    def baSearchTest(self):
        """ 按下查询按钮后开始执行 """
        self.resLabel.setText("按下查询按键！")
        label = ImageLabel(f"{current_path}/img/win_koyuki/banner/github.png", self)
        label.scaledToWidth(800)
        label.setBorderRadius(8, 8, 8, 8)
        self.scrollArea.horizontalScrollBar().setValue(0)
        self.scrollArea.setWidget(label)
        self.scrollArea.setFixedSize(800, 550)
    
        
        
        
class BaStudentSearchInterface(KoyukiInterface):
    def __init__(self, parent=None):
        super().__init__(
            title='碧蓝档案学生攻略查询',
            subtitle='资料来源：AronaBot(https://tutorial.arona.diyigemt.com/)',
            parent=parent
        )
        self.setObjectName('baSearchInterface')
        
        self.studentWikiView = StudentWikiView(self)
        self.vBoxLayout.addWidget(self.studentWikiView)