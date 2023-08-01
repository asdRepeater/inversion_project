from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui
import images_rc

class myMenu(QMenu):
    def __init__(self, parent=None, pos_policy=4):
        # 这里pos_policy设置6各方位。
        # 从1~6分别为左上，中上，右上，左下，中下，右下。
        # 给菜单设置按钮为父控件，这样就可以读取到按钮的尺寸信息
        super().__init__(parent)
        self.pos_policy = pos_policy

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        # point = self.pos() # 获取到全局的位置,这里应该获取的都是初始位置
        # x = point.x()
        # y = point.y()
        x = self.parent().x()
        y = self.parent().y() + self.parent().height()
        point = self.parent().parent().mapToGlobal(QPoint(x, y))
        x = point.x()
        y = point.y()
        # print(self.parent().x(), self.parent().y())
        # print(x, y)
        if self.pos_policy == 1:
            y = y - self.height() - self.parent().height()
            self.move(x, y)
            pass
        elif self.pos_policy == 2:
            x = x + (self.parent().width() - self.width())/2
            y = y - self.height() - self.parent().height()
            self.move(x, y)
            pass
        elif self.pos_policy == 3:
            x = x + (self.parent().width() - self.width())
            y = y - self.height() - self.parent().height()
            self.move(x, y)
            pass
        elif self.pos_policy == 4:
            pass
        elif self.pos_policy == 5:
            x = x + (self.parent().width() - self.width())/2
            self.move(x, y)
            pass
        elif self.pos_policy == 6:
            x = x + (self.parent().width() - self.width())
            self.move(x, y)
            pass
        # print(point)


class AboutUs(QToolButton):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initMenu()
        self.setup_ui_btn()

    def setTextColor(self, color):
        style = "QToolButton{color: " + color + ";} " + self.style
        self.setStyleSheet(style)

    def setMyIcon(self, ui_path):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(ui_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon1)

    def setup_ui_btn(self):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/welcome_pane/images/aboutus3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon1)
        # self.about_us_btn.setCheckable(True)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setObjectName("about_us_btn")
        self.setFixedSize(80, 30)
        self.setText(' 关于')
        # self.clicked.connect(self.showMenu) # 不需要手动连接这个槽函数
        self.setMenu(self.menu)
        # self.setArrowType(Qt.LeftArrow) # 这个arrow是一个图标

        self.setAutoRaise(True) # 这样就可以不用设置颜色什么的了
        self.style = "QToolButton:hover{color: #ff9500;background-color: transparent;} QToolButton:pressed{color: #ff9500;background-color: transparent;}"
        self.setStyleSheet(self.style)
        # self.setPopupMode(QToolButton.MenuButtonPopup)  # 设置弹出策略
        self.setPopupMode(QToolButton.InstantPopup)  # 设置弹出策略
        # print(self.popupMode())

        # 设置按钮动到父控件的左上角
        self.move(self.parent().width() - self.width(), 0)

    # def aboutUs(self):
    #     x = self.x()
    #     y = self.main_menus_qw.height()
    #     self.point = self.main_menus_qw.mapToGlobal(QPoint(x, y))
    #     self.menu.exec_(self.point)
    #     self.menu.close()
    #     pass
    def initMenu(self):
        self.menu = myMenu(self, 6)
        # self.menu = QMenu(self)
        # self.menu.setStyleSheet('QMenu::item{padding-left: 1px;}')
        # self.menu.setFixedWidth(self.open_files_btn.width() * 1.5)
        # self.menu.setFixedWidth(self.open_files_btn.width() * 2)
        # self.menu.setFixedWidth(140)
        # self.menu.setFixedHeight(100)

        open_models_action = QAction('软件版权信息',self)
        # open_models_action.triggered.connect(self.showInformation)
        self.menu.addAction(open_models_action)

        open_import_data_action = QAction('模型理论知识', self)
        # open_import_data_action.triggered.connect(self.showInformation)
        self.menu.addAction(open_import_data_action)

        open_export_data_action = QAction('帮助文档', self)
        # open_export_data_action.triggered.connect(self.showInformation)
        self.menu.addAction(open_export_data_action)

        self.triggered.connect(self.showInformation)
        self.menu.adjustSize()
        pass


    def showInformation(self, action):
        if not isinstance(action, QAction):
            return
        text = action.text()
        if text == '软件版权信息':
            QMessageBox.about(self, '你好', '我不好')
            pass
        elif text == '模型理论知识':
            QMessageBox.about(self, '你好', '我不好')
            pass
        elif text == '帮助文档':
            QMessageBox.about(self, '你好', '我不好')
            pass


if __name__ == '__main__':
    # 测试代码
    import sys
    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(500, 500)

    about_us = AboutUs(window)
    # about_us.move(410, 0)
    window.show()

    sys.exit(app.exec())