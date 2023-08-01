from PyQt5.Qt import *
from PyQt5 import QtCore
from resources.welcome_pane_ui import Ui_Form
from recent_browse import RecentBrowse
from xml_parse import readRecentBrowseXml
from about_us import *

class WelcomeInterface(QWidget, Ui_Form):
    model_select_signal = QtCore.pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_ui()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.initSlot()

    def setup_ui(self):
        self.top_qw.adjustSize() # 记住这个机制
        self.about_us_btn = AboutUs(self.top_qw)
        self.about_us_btn.setTextColor("white")
        train_list, predict_list = readRecentBrowseXml()
        train_recent_form = RecentBrowse(train_list, 6)
        v1_layout = QVBoxLayout()
        # v_layout.setSpacing(0)
        # v_layout.setContentsMargins(0,0,0,0)
        v1_layout.addWidget(train_recent_form)
        self.train_recent_qw.setLayout(v1_layout)
        predict_recent_form = RecentBrowse(predict_list, 6)
        v2_layout = QVBoxLayout()
        # v_layout.setSpacing(0)
        # v_layout.setContentsMargins(0,0,0,0)
        v2_layout.addWidget(predict_recent_form)
        self.predict_recent_qw.setLayout(v2_layout)

        self.train_recent_form = train_recent_form
        self.predict_recent_form = predict_recent_form
        pass

    def initSlot(self):
        self.model_train_btn.clicked.connect(lambda: self.model_select_signal.emit("train", ''))
        self.model_predict_btn.clicked.connect(lambda: self.model_select_signal.emit("predict", ''))
        # self.about_us_btn.clicked.connect(showAboutUsMenu)
        self.train_recent_form.model_name_signal.connect(lambda name: self.model_select_signal.emit("train", name))
        # self.train_recent_form.model_name_signal.connect(lambda name: print(name))
        self.predict_recent_form.model_name_signal.connect(lambda name: self.model_select_signal.emit("predict", name))


if __name__ == '__main__':
    # 测试代码
    import sys
    app = QApplication(sys.argv)

    window = WelcomeInterface()
    window.show()

    sys.exit(app.exec())