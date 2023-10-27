from typing import List
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, LargeTitleLabel,ImageLabel, VBoxLayout, line_edit, ToolTipFilter)
from .CONFIG import current_path
from .koyuki_interface import KoyukiInterface
from ..common.translator import Translator
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.trie import Trie

class BaDataInterface(KoyukiInterface):
    def __init__(self, parent=None):
        super().__init__(
            title='碧蓝档案国际服攻略',
            subtitle='资料来源：AronaBot(https://tutorial.arona.diyigemt.com/)',
            parent=parent
        )
        self.setObjectName('baDataInterface')
        
        self.w = SmoothScrollArea(parent)
        self.w.horizontalScrollBar().setValue(0)
        self.w.setFixedSize(775, 430)
        
        self.w2 = SmoothScrollArea(parent)
        self.w2.horizontalScrollBar().setValue(0)
        self.w2.setFixedSize(775, 430)

        
        card = self.addKoyukiCard(
            '测试卡片',
            self.w,
            'baidu.com'
        )
        card2 = self.addKoyukiCardWithoutSource(
            '测试卡片2',
            self.w2
        )
        
        card.card.installEventFilter(ToolTipFilter(card.card, showDelay=500))
        card.card.setToolTipDuration(2000)
        
        card2.card.installEventFilter(ToolTipFilter(card2.card, showDelay=50))
        card2.card.setToolTipDuration(2000)
        
        
