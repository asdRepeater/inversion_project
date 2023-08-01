import time

from PyQt5.Qt import *
from main_interface import MainInterface
from predict_interface import PredictInterface
from train_interface import TrainInterface
from welcome_interface import WelcomeInterface
# from visualization_interface import VisualizationInterface
from xml_parse import *

import sys
import os
import subprocess
import threading


background_application_initialize_time = 0


def logPrint(subp):
    main_window.standard_log_qtb.append('<---------------background application is launching--------------->\n')
    main_window.standard_log_qtb.append('waiting for response...(around 20 seconds)\n')
    # global flag
    # flag = 1
    # running_thread.start()
    # out, err = subp.communicate()
    # out = out.decode('utf-8')
    # err = err.decode('utf-8')
    # flag = 0
    # time.sleep(2)
    # log_window.textBrowser.append(out)
    # log_window.textBrowser.append(err)
    return_code = subp.poll()
    while return_code is None:
        out = subp.stdout.readline().strip()
        time.sleep(0.02)  # 这里加上睡眠后还可以刷新textBrowser界面，一举两得
        # subp.stdout.flush()
        try:
            out = out.decode('utf-8')
        except:
            out = out.decode('gbk')
        main_window.standard_log_qtb.append(out)    # 这里可能是当遇到中文时，自动按照gbk编码，所以utf-8不起作用了
        main_window.standard_log_qtb.moveCursor(main_window.standard_log_qtb.textCursor().End)
        return_code = subp.poll()
    # for i in iter(subp.stdout.readline, b''):
    #     tmp = i.rstrip()
    #     log_window.textBrowser.append(tmp.decode('utf-8'))
    #     # print(i.rstrip())

    # for line in iter(subp.stdout.readline, 'b'):
    #     print(line)
    #
    # subp.stdout.readline()
    main_window.model_train_btn.setEnabled(True)
    main_window.model_predict_btn.setEnabled(True)
    pass

# def errorPrint(subp):
#     main_window.error_log_qtb.append('<---------------background application is launching--------------->\n')
#     main_window.error_log_qtb.append('waiting for response...(around 20 seconds)\n')
#     # err = subp.stderr.read()
#     # log_window.error_browser.append(err.decode('utf-8'))
#     # time.sleep(0.5)
#     # log_window.error_browser.moveCursor(log_window.error_browser.textCursor().End)
#     return_code = subp.poll()
#     while return_code is None:
#         err = subp.stderr.readline().strip()
#         time.sleep(0.02)  # 这里加上睡眠后还可以刷新textBrowser界面，一举两得
#         # subp.stdout.flush()
#         try:
#             err = err.decode('utf-8')
#         except:
#             err = err.decode('gbk')
#         main_window.error_log_qtb.append(err) # utf-8对于中文的支持还是不太够
#         main_window.error_log_qtb.moveCursor(main_window.error_log_qtb.textCursor().End)
#         return_code = subp.poll()

def logPrint2(subp,para):
    train_window.start_train_btn.setEnabled(False)
    predict_window.start_predict_btn.setEnabled(False)
    main_window.standard_log_qtb.append('<---------------background application is launching--------------->\n')
    main_window.standard_log_qtb.append('waiting for response...(around 20 seconds)\n')
    return_code = subp.poll()
    while return_code is None:
        out = subp.stdout.readline().strip()
        time.sleep(0.02)  # 这里加上睡眠后还可以刷新textBrowser界面，一举两得
        try:
            out = out.decode('utf-8')
        except:
            out = out.decode('gbk')
        main_window.standard_log_qtb.append(out)    # 这里可能是当遇到中文时，自动按照gbk编码，所以utf-8不起作用了
        main_window.standard_log_qtb.moveCursor(main_window.standard_log_qtb.textCursor().End)
        return_code = subp.poll()
    pass
    # 训练完成时设置
    #

    train_window.start_train_btn.setEnabled(True)
    predict_window.start_predict_btn.setEnabled(True)
    if train_window.show_test_figure_cb.isChecked() and para == 'train':
        path = readTrainXML()['model_test']['save_path']
        main_window.show_tw.setCurrentIndex(2)
        main_window.picture_path_l.setText(path)
        pixmap = QPixmap(path)  # 按指定路径找到图片
        pixmap = pixmap.scaled(pixmap.width() * 1.2, pixmap.height()*1.2)
        main_window.picture_show_l.setPixmap(pixmap)  # 在label上显示图片
        # self.picture_show_l.setScaledContents(True)  # 让图片自适应大小
        main_window.picture_show_l.resize(pixmap.width(), pixmap.height())


# def errorPrint2(subp):
#     # main_window.error_log_qtb.append('<---------------background application is launching--------------->\n')
#     # main_window.error_log_qtb.append('waiting for response...(around 20 seconds)\n')
#     return_code = subp.poll()
#     while return_code is None:
#         err = subp.stderr.readline().strip()
#         time.sleep(0.02)  # 这里加上睡眠后还可以刷新textBrowser界面，一举两得
#         # subp.stdout.flush()
#         try:
#             err = err.decode('utf-8')
#         except:
#             err = err.decode('gbk')
#         main_window.standard_log_qtb.append(err) # utf-8对于中文的支持还是不太够
#         main_window.standard_log_qtb.moveCursor(main_window.error_log_qtb.textCursor().End)
#         return_code = subp.poll()


def callExe(para):
    # main_window.model_train_btn.setEnabled(False)
    # main_window.model_predict_btn.setEnabled(False)
    main_window.show_tw.setCurrentIndex(1)
    command = default_machine_learning_exe_path + ' ' + para
    # print(command)
    startup = subprocess.STARTUPINFO
    startup.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    subp = subprocess.Popen(command.split(' '), shell=False, creationflags=0x08000000, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 开启外部子进程
    # running_thread = threading.Thread(target=running, args=())
    log_thread = threading.Thread(target=logPrint2, args=(subp,para))
    log_thread.start()
    # error_thread = threading.Thread(target=errorPrint2, args=(subp,))
    # error_thread.start()
    # for line in subp.stdout.readlines():
    #     print(line)
    # subp.stdout.close()
    # pass
    # 打开日志窗口
    # log_window.show()

def train_window_show(method_name):
    train_window.main_train_title_l.setText(method_name + '-模型训练')
    method_name = method_name[method_name.find('(') + 1:method_name.find(')')]
    train_window.parameter_list.showForm(method_name) # 内部自动将子控件和父控件自适应调整大小
    predict_window.hide()
    train_window.show()
    if train_window.parameter_list.current_model == 'MTL' or train_window.parameter_list.current_model == 'ST-MTL':
        train_window.y_path_le.setPlaceholderText("注：此处文件夹路径数量>=2")
        train_window.y_path_le.setText('')
    # print(train_window.parameter_list_qw.height())
    else:
        train_window.y_path_le.setPlaceholderText("")
    main_window.show_tw.setCurrentIndex(0)

def predict_window_show(model_name):
    # print('asd')
    predict_window.main_predict_title_l.setText(model_name + '-模型推理')
    predict_window.current_model = model_name
    predict_window.setModelInfo()
    train_window.hide()
    predict_window.show()
    main_window.show_tw.setCurrentIndex(0)


def main_window_show(type, name):
    welcome_window.close()
    if type == 'train' and name != '':
        main_window.model_tw.setCurrentIndex(0)
        for i in main_window.tab_1.findChildren(QPushButton):
            if i.text() == name:
                train_window_show(name)
                break
        pass
    elif type == 'predict' and name != '':
        main_window.model_tw.setCurrentIndex(1)
        for i in main_window.tab_2.findChildren(QPushButton):
            if i.text() == name:
                predict_window_show(name)
                break
        pass
    elif type == 'train' and name == '':
        main_window.model_tw.setCurrentIndex(0)
        pass
    elif type == 'predict' and name == '':
        main_window.model_tw.setCurrentIndex(1)
    main_window.show()

if __name__ == '__main__':
    # 运行程序(UI模块与业务逻辑模块的交互都在这里进行)

    app = QApplication(sys.argv)

    # 初始化项目文件夹,欢迎界面最近浏览，
    initDir()
    initRecentBrowseXml()

    # 创建窗口
    welcome_window = WelcomeInterface()
    main_window = MainInterface()
    predict_window = PredictInterface()
    train_window = TrainInterface()
    main_window.tab_3_layout.addWidget(train_window)
    main_window.tab_3_layout.addWidget(predict_window)
    train_window.hide()
    predict_window.hide()
    # visualization_window = VisualizationInterface()

    # 连接信号与槽

    main_window.model_select_btn_signal.connect(predict_window_show)
    main_window.method_select_btn_signal.connect(train_window_show)


    train_window.start_train_btn_signal.connect(callExe)
    predict_window.start_predict_btn_signal.connect(callExe)

    welcome_window.model_select_signal.connect(main_window_show)

    # main_window.show()

    welcome_window.show()

    sys.exit(app.exec())




