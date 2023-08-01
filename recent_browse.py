from PyQt5.Qt import *
from PyQt5 import QtCore



class RecentBrowse(QWidget):
    model_name_signal = QtCore.pyqtSignal(str)
    def __init__(self, menu_list, show_num):
        super().__init__()
        self.menu_list = menu_list
        self.show_num = show_num
        self.menu = QMenu()
        self.menu.close()
        self.setup_ui()


    def setup_ui(self):
        v_layout = QVBoxLayout()
        # v_layout.setSpacing(0)
        # v_layout.setContentsMargins(0,0,0,0)
        self.setLayout(v_layout)
        self.v_layout = v_layout

        load_btn = QPushButton('加载更多...')
        load_btn.clicked.connect(self.showMenu)
        load_btn.setFixedSize(500, 30)
        load_btn.setStyleSheet(
            'QPushButton{background-color: transparent; text-align: center; font-weight: bold;} QPushButton:hover{text-decoration:underline;} QPushButton:pressed{font-weight: bold;}')
        self.v_layout.addWidget(load_btn)
        self.load_btn = load_btn

        self.createMenu()
        self.createBtn()
        # self.setFixedHeight(30 * self.show_num)



    def createMenu(self):
        # print(self.menu.height)
        for i in range(len(self.menu_list)):
            action = QAction(self)
            action.setText(self.menu_list[i])
            action.triggered.connect(self.modelNameSlot)
            self.menu.addAction(action)
        # self.menu.setStyleSheet('QMenu::item{height: 34px;width: 120px; padding-left: 30px;}')
        self.menu.adjustSize() # 感觉menu里面应该是有布局的，所以要adjustsize
        # print(self.menu.height)


    def createBtn(self):
        max_num = self.show_num
        current_num = len(self.menu_list)
        # 用空按钮去代替，这样布局就不会有问题
        for i in range(max_num):
            try:
                btn = QPushButton(self.menu_list[i])
                btn.setFixedSize(500, 30)
                btn.clicked.connect(self.modelNameSlot)
                if btn.fontMetrics().width(self.menu_list[i]) <= 500:
                    btn.setStyleSheet(
                        'QPushButton{background-color: transparent; text-align: center;} QPushButton:hover{text-decoration:underline;}')
                else:
                    btn.setStyleSheet(
                        'QPushButton{background-color: transparent; text-align: left;} QPushButton:hover{text-decoration:underline;}')
                self.v_layout.insertWidget(i, btn)
            except:
                btn = QPushButton()
                btn.setFixedSize(500, 30)
                btn.setStyleSheet(
                    'QPushButton{background-color: transparent;}')
                self.v_layout.insertWidget(i, btn)


    def showMenu(self):
        # print(self.menu.height())
        x = self.load_btn.x() + (self.load_btn.width() - self.menu.width()) / 2
        y = self.load_btn.y() - self.menu.height()
        dest_point = self.mapToGlobal(QPoint(x, y))
        self.menu.exec_(dest_point)

    def modelNameSlot(self):
        # print(self.sender().text())
        self.model_name_signal.emit(self.sender().text())

if __name__ == '__main__':
    # 测试代码
    import sys
    app = QApplication(sys.argv)

    window = RecentBrowse(['asd', 'asd1', 'asd2', 'asd3', 'asd4'], 3)
    window.show()

    sys.exit(app.exec())