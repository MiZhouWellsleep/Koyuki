from typing import List
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot , QTimer, QThread
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, LargeTitleLabel,ImageLabel, VBoxLayout, line_edit, ToolTipFilter,
                            PushButton)
from .CONFIG import current_path
from .koyuki_interface import KoyukiInterface, KoyukiCard, KoyukiCardWithoutSource
from ..common.translator import Translator
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.trie import Trie

import requests
import json
from io import BytesIO
from PIL import Image
from .CONFIG import COMMON_LOADING, COMMON_ERROR

timeout_time = 30

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
            response_img = requests.get(self.res_url, timeout=timeout_time)
            image_data = response_img.content
            image = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(image)
            # image_data = BytesIO(response_img.content)
            # pil_image = Image.open(image_data)
            # pil_image = pil_image.convert("RGBA")
            # pixmap = QPixmap.fromImage(QImage(pil_image.tobytes(), pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888))
        except:
            pixmap = QPixmap(COMMON_ERROR)
        self.imageFetched.emit(pixmap)
        self.fetchingFinished.emit()

class StartCard(KoyukiCardWithoutSource):
    updateDataCard = pyqtSignal(str)
    def __init__(self, parent=None):
        self.parent = parent
        self.btn = PushButton('刷新数据')
        super().__init__(
            title='按下按钮更新国际服最新攻略',
            widget=self.btn
        )
        self.updateDataCard.connect(self.parent.updateData)
        self.btn.clicked.connect(self.sendValue)
        
    @pyqtSlot()
    def sendValue(self):
        self.updateDataCard.emit(None)

class DataCard(KoyukiCard):
    def __init__(self, title, imgUrl, stretch=0, parent=None):
        self.w = SmoothScrollArea(parent)
        super().__init__(
            parent=parent,
            title=title,
            widget=self.w,
            sourcePath=imgUrl,
            stretch=stretch
            )
        self.imgUrl = imgUrl
        self.fetch_thread = None
        
        self.dataImg = ImageLabel(f"{current_path}/img/win_koyuki/banner/header1.png", self)
        self.dataImg.scaledToWidth(775)
        self.dataImg.setBorderRadius(8, 8, 8, 8)
        self.w.horizontalScrollBar().setValue(0)
        self.w.setWidget(self.dataImg)
        self.w.setFixedSize(775, 430)
        
        
    def showNewData(self):
        responseImg = requests.get(self.imgUrl, timeout=timeout_time)
        # image_data = BytesIO(responseImg.content)
        # pil_image = Image.open(image_data)
        # pil_image = pil_image.convert("RGBA")
        # pixmap = QPixmap.fromImage(QImage(pil_image.tobytes(), pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888))
        image_data = responseImg.content
        image = QImage.fromData(image_data)
        pixmap = QPixmap.fromImage(image)
        self.dataImg.setPixmap(pixmap)
        self.dataImg.scaledToWidth(800)
        
    def fetch_image(self):
        if self.fetch_thread is not None:
            self.fetch_thread.quit()
            self.fetch_thread.wait()
        self.fetch_thread = FetchImageThread(self.imgUrl)
        self.fetch_thread.imageFetched.connect(self.showData)
        self.fetch_thread.fetchingStarted.connect(self.fetching_start)
        #self.fetch_thread.fetchingFinished.connect(self.fetching_finish)
        self.fetch_thread.start()
    def showData(self, pixmap):
        self.pixmap = pixmap
        self.dataImg.setPixmap(pixmap)
        self.dataImg.scaledToWidth(775)
    def fetching_start(self):
        self.showData(QPixmap(COMMON_LOADING))
        


class BaDataInterface(KoyukiInterface):
    def __init__(self, parent=None):
        super().__init__(
            title='碧蓝档案国际服攻略',
            subtitle='资料来源：AronaBot(https://tutorial.arona.diyigemt.com/)',
            parent=parent
        )
        self.setObjectName('baDataInterface')
        url = 'https://arona.cdn.diyigemt.com/image'
        
        cardStart = StartCard(self)
        self.vBoxLayout.addWidget(cardStart, 0, Qt.AlignTop)
        
        self.card_huodong = DataCard('国际服活动', url + self.activitySearch())
        self.vBoxLayout.addWidget(self.card_huodong, 0, Qt.AlignTop)
        
        self.card_zongli = DataCard('国际服总力战', url + '/some/国际服总力.png')
        self.vBoxLayout.addWidget(self.card_zongli, 0, Qt.AlignTop)
        
        self.card_huoli = DataCard('国际服火力演习', url + '/some/国际服火力演习.png')
        self.vBoxLayout.addWidget(self.card_huoli, 0, Qt.AlignTop)
        
        self.card_jjc = DataCard('国际服竞技场', url + '/some/日服竞技场.png')
        self.vBoxLayout.addWidget(self.card_jjc, 0, Qt.AlignTop)
        
        self.card_weilai = DataCard('国际服未来视', url + '/some/国际服未来视.png')
        self.vBoxLayout.addWidget(self.card_weilai, 0, Qt.AlignTop)
        
        self.card_renquan = DataCard('国际服人权', url + '/some/日服人权.png')
        self.vBoxLayout.addWidget(self.card_renquan, 0, Qt.AlignTop)
        
    
    def activitySearch(self):
        """ 获取国际服最新活动攻略地址 """
        url = "https://arona.diyigemt.com/api/v1/image?name=国际服活动"
        try:
            response_data = requests.get(url, timeout=timeout_time)
            response_data.raise_for_status()
            response_data.encoding = response_data.apparent_encoding
            json_data = response_data.json()
            return json_data['data'][0]['path']
        except:
            return 'ERROR'
        
    def updateData(self):
        self.card_huodong.fetch_image()
        self.card_zongli.fetch_image()
        self.card_huoli.fetch_image()
        self.card_jjc.fetch_image()
        self.card_weilai.fetch_image()
        self.card_renquan.fetch_image()
        
