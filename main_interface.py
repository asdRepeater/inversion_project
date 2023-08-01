
from PyQt5.Qt import *
from resources.main_pane_ui import Ui_Form
from PyQt5 import QtCore
from xml_parse import *
from about_us import *
import sys
import os
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np

class MainInterface(QWidget, Ui_Form):
    model_train_btn_signal = QtCore.pyqtSignal()
    model_predict_btn_signal = QtCore.pyqtSignal()
    visualizing_btn_signal = QtCore.pyqtSignal()
    method_select_btn_signal = QtCore.pyqtSignal(str)
    model_select_btn_signal = QtCore.pyqtSignal(str)
    #
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # print(self.size(), self.main_menus_qw.size())
        # self.main_menus_qw.resize(self.main_menus_qw.size())
        # print(self.main_menus_qw.size())
        self.about_us_btn.move(self.width() - self.about_us_btn.width(), 0)


        pass
    def closeEvent(self, a0: QCloseEvent) -> None:
        app = QApplication.instance()
        app.quit()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        # self.open_files_btn.installEventFilter(self)
        # self.menu.installEventFilter(self)
        self.initModels()
        # self.initMutexToolBtn()
        self.initLogInterface()
        # self.showMaximized()
        self.setWindowState(Qt.WindowMaximized)
        self.setup()

    def setup(self):
        # self.main_menus_qw.adjustSize()
        # print(self.main_menus_qw.size()) # 这个size是潜在的尺寸，咱要获取当前尺寸
        # print(self.main_menus_qw.geometry())
        self.about_us_btn = AboutUs(self.main_menus_qw)
        self.about_us_btn.setTextColor("black")
        self.tab_3_layout = QVBoxLayout()
        self.tab_3.setLayout(self.tab_3_layout)
        # 设置tab的展示顺序
        self.model_tw.setCurrentIndex(0)
        self.show_tw.setCurrentIndex(0)
        # 设置刷新自定义菜单
        self.tab_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_2.customContextMenuRequested.connect(self.showMenu)
        # self.error_log_qtb.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.error_log_qtb.customContextMenuRequested.connect(self.showMenu)
        # 设置菜单行为

        self.refresh_menu = QMenu(self)
        refresh_action = QAction(self)
        refresh_action.setText('刷新')
        refresh_action.triggered.connect(self.refresh)
        self.refresh_menu.addAction(refresh_action)
        self.tab_2.setProperty('menu', self.refresh_menu)

    def showMenu(self, point):
        point = self.sender().mapToGlobal(point)
        # self.point = self.main_menus_qw.mapToGlobal(QPoint(self.log_btn.x(), self.main_menus_qw.height()))
        self.sender().property('menu').exec_(point)

    def refresh(self):
        for i in self.model_tw.widget(1).findChildren(QPushButton):
            i.setParent(None)  # 记住这个，只要没有父引用，直接销毁，666
        # for i in self.model_tw.widget(1).children():
        #     print(i)
        self.exist_models = [i[:-4] for i in os.listdir(default_export_model_dir)]
        for i in range(len(self.exist_models)):
            btn = QPushButton(self.exist_models[i], self.model_tw.widget(1))
            btn.setFixedSize(310, 30)
            btn.move(0, i * 30)
            stylesheet = 'QPushButton{border:none;border-bottom: 1px solid rgba(0,0,0,0.1); font-size: 12px; text-align: left;} QPushButton:hover{background-color: rgba(204, 232, 255, 0.5);} QPushButton:pressed{background-color: rgba(204, 232, 255, 1);}'
            btn.setStyleSheet(stylesheet)
            btn.clicked.connect(self.modelSelection)
            btn.setToolTip(self.exist_models[i])
            btn.show()

    def modelPredict(self):
        self.model_predict_btn_signal.emit()
        pass
    def modelTrain(self):
        self.model_train_btn_signal.emit()
        pass

    # def eventFilter(self, watched, event):
    #     if event.type() == QtCore.QEvent.HoverEnter and watched == self.open_files_btn:
    #         # self.menu.setFocus()
    #         self.open_files_btn.clearFocus()
    #         self.point = self.main_menus_qw.mapToGlobal(QPoint(0, self.main_menus_qw.height()))
    #         self.menu.exec_(self.point)
    #
    #         return True
    #     elif event.type() == QtCore.QEvent.HoverLeave and watched == self.open_files_btn:
    #         self.menu.close()
    #         return True
    #     elif event.type() == QtCore.QEvent.HoverLeave and watched == self.menu:
    #         print('out')
    #     elif event.type() == QtCore.QEvent.FocusOut and watched == self.menu:
    #         print(watched)
    #         print('in')
    #         return True
    #     return False


    # def openImportData(self):
    #     self.open_files_btn.setChecked(False)
    #     path = QFileDialog.getOpenFileName(self, '打开导入数据', default_import_data_dir, '表格数据(*.csv *.xls *.xlsx *.txt)', '表格数据(*.csv *.xls *.xlsx *.txt)')[0]
    #     if path != '':
    #         path = '"' + path + '"'
    #         os.popen(path)
    #
    # def openExportData(self):
    #     self.open_files_btn.setChecked(False)
    #     path = QFileDialog.getOpenFileName(self, '打开导出数据', default_export_data_dir, '表格或图像(*.csv *.jpg)', '表格或图像(*.csv *.jpg)')[0]
    #     if path != '':
    #         path = '"' + path + '"'
    #         os.popen(path)
    #
    # def openModels(self):
    #     self.open_files_btn.setChecked(False)
    #     path = QFileDialog.getOpenFileName(self, '打开我的模型', default_export_model_dir, '模型二进制文件(*.pkl)', '模型二进制文件(*.pkl)')[0]
    #     if path != '':
    #         QMessageBox.about(self, '提示', '功能尚未完善，请谅解！')
    #         pass    # 这里的处理暂时搁置

    # def openPreprocessingData(self):
    #     self.open_files_btn.setChecked(False)
    #     path = QFileDialog.getOpenFileName(self, '打开预处理数据', default_preprocessing_dir, '表格或图像(*.csv *.tif *.tiff *.jpg)', '表格或图像(*.csv *.tif *.tiff *.jpg)')[0]
    #     if path != '':
    #         path = '"' + path + '"'
    #         os.popen(path)

    def initModels(self):
        model_cn_name = readCnName()
        self.models = list(model_cn_name.keys())
        for i in range(len(self.models)):
            btn = QPushButton(model_cn_name[self.models[i]] + '(' + self.models[i] + ')', self.model_tw.widget(0))
            btn.setFixedSize(310, 30)
            btn.move(0, i * 30)
            stylesheet = 'QPushButton{border:none;border-bottom: 1px solid rgba(0,0,0,0.1); font-size: 20px; text-align: left;} QPushButton:hover{background-color: rgba(204, 232, 255, 0.5);} QPushButton:pressed{background-color: rgba(204, 232, 255, 1);}'
            btn.setStyleSheet(stylesheet)
            btn.clicked.connect(self.methodSelection)
        # 下面是模型名称列表
        self.exist_models = [i[:-4] for i in os.listdir(default_export_model_dir)]
        for i in range(len(self.exist_models)):
            btn = QPushButton(self.exist_models[i], self.model_tw.widget(1))
            btn.setFixedSize(310, 30)
            btn.move(0, i * 30)
            stylesheet = 'QPushButton{border:none;border-bottom: 1px solid rgba(0,0,0,0.1); font-size: 12px; text-align: left;} QPushButton:hover{background-color: rgba(204, 232, 255, 0.5);} QPushButton:pressed{background-color: rgba(204, 232, 255, 1);}'
            btn.setStyleSheet(stylesheet)
            btn.clicked.connect(self.modelSelection)
            btn.setToolTip(self.exist_models[i])

        # scroll1 = QScrollArea(self.model_tw.widget(0))
        # scroll1.setWidget(self.model_tw.widget(0))
        # scroll2 = QScrollArea(self.model_tw.widget(1))
        # scroll2.setWidget(self.model_tw.widget(1))

    def methodSelection(self):
        self.method_select_btn_signal.emit(self.sender().text())
        # print(self.sender().text())
        pass
    def modelSelection(self):
        self.model_select_btn_signal.emit(self.sender().text())


    def initMutexToolBtn(self):
        # self.tool_btn_group = QButtonGroup(self)
        # self.tool_btn_group.setExclusive(True)
        # self.tool_btn_group.addButton(self.train_toolbtn)
        # self.tool_btn_group.addButton(self.predict_toolbtn)
        pass


    # 初始化日志界面
    # def showLog(self, checked):
    #     # self.log_btn_signal.emit()
    #     if checked:
    #         self.point = self.main_menus_qw.mapToGlobal(QPoint(self.log_btn.x(), self.main_menus_qw.height()))
    #         self.menu2.exec_(self.point)
    #     else:
    #         self.menu2.close()
    # #     pass
    # def showMenu(self, point):
    #     point = self.standard_log_qtb.mapToGlobal(point)
    #     # self.point = self.main_menus_qw.mapToGlobal(QPoint(self.log_btn.x(), self.main_menus_qw.height()))
    #     self.log_menu.exec_(point)

    def initLogInterface(self):
        # 设置自定义菜单
        self.standard_log_qtb.setContextMenuPolicy(Qt.CustomContextMenu)
        self.standard_log_qtb.customContextMenuRequested.connect(self.showMenu)
        # self.error_log_qtb.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.error_log_qtb.customContextMenuRequested.connect(self.showMenu)
        # 设置菜单行为
        self.log_menu = QMenu(self)
        copy_action = QAction(self)
        copy_action.setText('复制')
        copy_action.triggered.connect(lambda: self.standard_log_qtb.copy())
        self.log_menu.addAction(copy_action)
        save_action = QAction(self)
        save_action.setText('保存日志')
        save_action.triggered.connect(self.saveLog)
        self.log_menu.addAction(save_action)
        clear_action = QAction(self)
        clear_action.setText('清除日志')
        clear_action.triggered.connect(lambda: self.standard_log_qtb.clear())
        self.log_menu.addAction(clear_action)
        select_all_action = QAction(self)
        select_all_action.setText('选择全部')
        select_all_action.triggered.connect(lambda: self.standard_log_qtb.selectAll())
        self.log_menu.addAction(select_all_action)
        import_log_action = QAction(self)
        import_log_action.setText('导入日志')
        import_log_action.triggered.connect(self.importLog)
        self.log_menu.addAction(import_log_action)

        self.standard_log_qtb.setProperty('menu', self.log_menu)
        # clear_error_log_action = QAction(self)
        # clear_error_log_action.setText('清除错误日志')
        # clear_error_log_action.triggered.connect(lambda: self.error_log_qtb.clear())
        # self.menu3.addAction(clear_error_log_action)

    def saveLog(self):
        path = QFileDialog.getSaveFileName(self, '保存日志', BASE_DIR, '日志(*.txt)', '日志(*.txt)')[0]
        if path != '':
            with open(path, 'w') as f:
                f.write(self.sender().toPlainText())
            self.standard_log_qtb.append('(log has been saved)')

    def importLog(self):
        path = QFileDialog.getOpenFileName(self, '导入日志', BASE_DIR, '日志(*.txt)', '日志(*.txt)')[0]
        if path != '':
            with open(path, 'r') as f:
                self.standard_log_qtb.append(f.read())


    # 可视化
    def showPictureBtn(self):
        path = QFileDialog.getOpenFileName(self, '导入图像', default_export_tif_dir, '(*.jpg *.png)', '(*.jpg *.png)')[0]
        dirStr, ext = os.path.splitext(path)
        if path != '':
            if ext == 'jpg' or ext == 'png':
                self.picture_path_l.setText(path)
                pixmap = QPixmap(path)  # 按指定路径找到图片
                pixmap = pixmap.scaled(pixmap.width() * 1.2, pixmap.height() * 1.2)
                self.picture_show_l.setPixmap(pixmap)  # 在label上显示图片
                # self.picture_show_l.setScaledContents(True)  # 让图片自适应大小
                self.picture_show_l.resize(pixmap.width(), pixmap.height())
            elif ext == 'tif':
                pass

    def read_img(filename):
        dataset = gdal.Open(filename)  # 打开文件
        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数
        im_bands = dataset.RasterCount  # 波段数
        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
        im_proj = dataset.GetProjection()  # 地图投影信息，字符串表示
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)

        del dataset

        # print(im_width, im_height, '\n', im_bands,  '\n', im_proj,  '\n', im_geotrans,  '\n', im_data)
        # print(type(im_data), im_data.dtype, im_data.dtype.name, im_data.shape)
        # print(im_proj)
        return im_width, im_height, im_bands, im_proj, im_geotrans, im_data

    # def showGeoTiff(tiff_path, title=''):
    #     im_width, im_height, im_bands, im_proj, im_geotrans, im_data = self.read_img(tiff_path)
    #     plt.ioff()
    #     plt.rcParams["font.family"] = "SimHei"
    #     # print(im_data)
    #     im_data = np.where(im_data < 0, 0, im_data)
    #     # print(np.min(im_data), np.max(im_data), np.max(im_data)-np.min(im_data))
    #     im_data = (im_data - np.min(im_data)) / (np.max(im_data) - np.min(im_data)) * 255
    #     # print(im_data)
    #     # plt.imshow(im_data)
    #     if title != '':
    #         plt.title(title)
    #     else:
    #         title = readFileName(tiff_path)
    #         plt.title(title)

if __name__ == '__main__':
    # 测试代码
    import sys
    app = QApplication(sys.argv)

    window = MainInterface()
    window.show()

    sys.exit(app.exec())

    # ****************************** 开始

    # ****************************** 结束