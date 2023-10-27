import os
import sys
import random
import typing
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import pygame
import os
from qfluentwidgets import RoundMenu, FluentIcon, Action, FluentTranslator

from windows.win_koyuki import WinKoyuki

##########################
# 全局初始参数
##########################
init_img = "img/1.png"
init_voice = "music/1/1.1.ogg"

init_koyuki_size = 200

##########################
# 小雪窗口
##########################
class Koyuki(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Koyuki, self).__init__(parent)
        # 窗体初始化
        self.init()
        # 加入成员变量
        self.initSubwin()
        # 托盘化初始
        self.initPall()
        # 待机gif加载
        self.initYukiImage()
        # 待机动画
        self.yukiNormalAction()
        
        # 窗体初始化
    def init(self):
        # 初始化
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        # https://blog.csdn.net/kaida1234/article/details/79863146
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.any = 0

        # 重绘组件、刷新
        self.repaint()
        
    # 将所有子窗口添加入成员变量
    def initSubwin(self):
        self.win_koyuki = None
        # 下面是加入的一些成员变量
        self.is_showing = 1

    # 托盘化设置初始化
    def initPall(self):
        quit_action = QAction('退出', self, triggered=self.quit)
        show_action = QAction('显示与隐藏', self, triggered=self.showwin)
        
        quit_action.setIcon(QIcon(init_img))
        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(show_action)
        
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(init_img))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)

        # 展示
        self.tray_icon.show()
    
    def initYukiImage(self):
        # 对话框定义
        self.talkLabel = QLabel(self)
        # 对话框样式设计
        self.talkLabel.setStyleSheet("font:25pt '楷体';border-width: 1px;color:blue;")
        # 定义显示图片部分
        self.image = QLabel(self)
        # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
        self.movie = QMovie(init_img)
        # 设置标签大小
        self.movie.setScaledSize(QSize(init_koyuki_size, init_koyuki_size))
        # 将Qmovie在定义的image中显示
        self.image.setMovie(self.movie)
        self.movie.start()
        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.talkLabel)
        layout.addWidget(self.image)
        layout.setAlignment(self.talkLabel, Qt.AlignCenter)
        layout.setAlignment(self.image, Qt.AlignCenter)
        self.setLayout(layout)
        self.resize(1024, 100)
        # 调用自定义的randomPosition，会使得小雪出现位置随机
        ## self.randomPosition()
        # 展示
        self.show()
            
    # 正常待机动作
    def yukiNormalAction(self):
        # 每隔一段时间做个动作
        # 定时器设置
        self.timer = QTimer()
        # 时间到了自动执行
        self.timer.timeout.connect(self.randomAct)
        # 动作时间切换设置
        self.timer.start(3000)
        # 小雪状态设置为正常
        self.condition = 0
        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(3000)
        # 对话状态设置为常态
        
        self.is_changing = 0
       
    ##########################
    # 自定义基础工具函数
    ########################## 
    def yuki_change(self, img_path, text=None, voice_path=None):
        # 图片或gif更改
        self.movie = QMovie(img_path)
        self.movie.setScaledSize(QSize(init_koyuki_size, init_koyuki_size))
        self.image.setMovie(self.movie)
        self.movie.start()
        # 对话更改
        if text != None:
            self.talkLabel.setText(text)
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:25pt '楷体';"
                "color:pink;"
                "background-color: black"
                "url(:/)"
            )
            self.talkLabel.adjustSize()
        # 声音播放
        if voice_path != None:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(voice_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            
    def talk(self, img_path=init_img, text=None, voice_path=None):
        if self.is_changing:
            self.yuki_change(img_path, text, voice_path)
            self.is_changing = 0
        else:
            self.yuki_change(init_img, "", None)
            
            
    ##########################
    # 自定义函数
    ##########################
    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()
    # 控制小雪显示与隐藏（通过控制透明度）
    def showwin(self):
        if self.is_showing:
            self.setWindowOpacity(0)
            self.is_showing = 0
        else:
            self.setWindowOpacity(1)
            self.is_showing = 1
    
    def randomAct(self):
        pass
    
    
    ##########################
    # 鼠标事件
    ##########################
    # 鼠标左键按下时, 小雪将和鼠标位置绑定
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 小雪状态发生变化
            self.is_changing = 1
            
        self.talk("img/3.png", "碧蓝档案", init_voice)
           
        
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.OpenHandCursor))
        
    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if Qt.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)
    
    # 防止子窗口关闭后小雪也跟着关闭
    def closeEvent(self, event):
        # 忽略关闭事件，防止主界面关闭
        event.ignore()
        
    # 鼠标右键点击交互
    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)
        # 添加菜单项目
        action_koyuki = Action(QIcon("img/1.png"), "小雪功能面板")
        action_showwin = Action(FluentIcon.UP, "隐藏")
        action_quit = Action(FluentIcon.CLOSE, "退出")
        
        menu.addActions([
            action_koyuki,
            action_showwin,
            action_quit
        ])
        # 绑定菜单功能
        action_koyuki.triggered.connect(self.func_koyuki)
        action_showwin.triggered.connect(self.showwin)
        action_quit.triggered.connect(self.func_quit)
               
        menu.exec(e.globalPos())
        
    # 右键菜单的相关函数    
    def func_quit(self):
        self.yuki_change("img/8.png", "再见了捏", "music/test/ji.ogg")
        # 间隔几秒等语音播出完后再关闭，待修改
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(qApp.quit)
        timer.start(2200)
    def func_koyuki(self):
        #self.yuki_change("img/6.png", "test", "music/1/1.1.ogg")
        #self.yuki_change("img/3.png", "测试2", "music/1/1.2.ogg")
        self.yuki_change("img/3.png", "小雪功能面板，启动", "music/1/1.1.ogg")
        if self.win_koyuki is None:
            self.win_koyuki = WinKoyuki(self)
        self.win_koyuki.show()

        
if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    
    translator = FluentTranslator()
    app.installTranslator(translator)

    pet = Koyuki()
    sys.exit(app.exec_())    