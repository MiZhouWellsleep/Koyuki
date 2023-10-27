from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon
import os

from .CONFIG import current_path
from ..components.link_card import LinkCardView
from ..common.style_sheet import StyleSheet



class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.koyukiLabel = QLabel('KOYUKI', self)
        self.banner = QPixmap(f'{current_path}\img\win_koyuki\\banner\header.png')
        self.linkCardView = LinkCardView(self)

        self.koyukiLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.koyukiLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # 添加链接标签
        self.linkCardView.addCard(
            f'{current_path}\img\win_koyuki\\banner\\bilibili.jpg',
            self.tr('米粥的b站'),
            self.tr('关注米粥今晚要早睡喵，关注米粥今晚要早睡谢谢喵（虽然基本不发东西。。）'),
            "https://space.bilibili.com/405999287"
        )
        self.linkCardView.addCard(
            f'{current_path}\img\win_koyuki\\banner\github.png',
            self.tr('米粥的github'),
            self.tr('这位更是顶级懒狗。。'),
            "https://github.com/MiZhouWellsleep"
        )
        self.linkCardView.addCard(
            f'{current_path}\img\win_koyuki\\banner\PyQt-Fluent-Widgets.png',
            self.tr('PyQt-Fluent-Widgets'),
            self.tr('超级好用的基于PyQt5的Fluent Design风格组件库!'),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets'
        )
        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr("参考项目"),
            self.tr("最初想搞个python桌宠没啥头绪，搜到这个看着模仿着搞的，虽然现在貌似搞歪了。。"),
            'https://github.com/mf22221111/klee_python'
        )
        

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # draw background color
        if not isDarkTheme():
            painter.fillPath(path, QColor(206, 216, 228))
        else:
            painter.fillPath(path, QColor(0, 0, 0))

        # draw banner image
        aspect_ratio = self.banner.width() / self.banner.height()
        target_width = self.width()
        target_height = int(target_width / aspect_ratio)
        target_y = (h - target_height) // 2 + 50
        #target_y = 0

        target_rect = QRectF(0, target_y, target_width, target_height)
        source_rect = QRectF(0, 0, self.banner.width(), self.banner.height())

        painter.drawPixmap(target_rect, self.banner, source_rect)
        
class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        pass