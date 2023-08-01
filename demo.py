# import os
# 
# from PyQt5.Qt import *
# 
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('测试')
#         self.resize(500, 500)
#         self.setup_ui()
# 
#     def setup_ui(self):
#         pass
# 
# 
# 
# if __name__ == '__main__':
#     # 测试代码
#     # import sys
#     # app = QApplication(sys.argv)
#     #
#     # window = Window()
#     # window.show()
#     #
#     # str = '123'
#     #
#     # print(str.find('2'))
#     #
#     # sys.exit(app.exec())
# 
#     import time
# 
#     # t = '2020-4-06 00:00:00'
#     # s_t = time.strptime(t, "%Y-%m-%d %H:%M:%S")  # 返回元祖
#     # mkt1 = int(time.mktime(s_t))
#     # print(mkt1)
#     # t = '2020-4-06 01:00:00'
#     # s_t = time.strptime(t, "%Y-%m-%d %H:%M:%S")  # 返回元祖
#     # mkt2 = int(time.mktime(s_t))
#     # print(mkt2)
#     # print(mkt2 - mkt1)
# 
#     # str1 = '434-123'
#     # print(str(str1.split('-')))
#     #
#     # print(os.listdir('G:\software_development\inversion_project\import_data\pm'))
#     #
#     import datetime
#     # t = datetime.time(1, 10, 20, 13)
#     # print(t, type(t))
#     #
#     #
#     # x = datetime.datetime(2018, 9, 15, 1)
#     # y = datetime.datetime(2018, 10, 1, 1)
#     # print(x, type(x), y - x, x)
#     #
#     # # # 方式二
#     # d_time = datetime.datetime.now()
#     # un_time = time.mktime(d_time.timetuple())
#     # print(un_time, type(un_time))
#     # # 将unix时间戳转换为“当前时间”格式
#     # times = datetime.datetime.fromtimestamp(un_time)
#     # print(times, type(times), str(times), type(str(times)))
#     #
#     # print(int('09'))
# 
#     def timestampProcess(research_time):
#         start = research_time[0]
#         end = research_time[1]
#         # print(start.strptime('%Y-%m-%d %H:%M'))
#         # print(time.strptime(start, '%Y%m%d%H'))
#         start_time = datetime.datetime(int(start[0:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]))
#         end_time = datetime.datetime(int(end[0:4]), int(end[4:6]), int(end[6:8]), int(end[8:10]))
#         start_stamp = time.mktime(start_time.timetuple())
#         end_stamp = time.mktime(end_time.timetuple())
#         result = []
#         hours = int(((end_stamp - start_stamp) / 3600))
#         for i in range(hours + 1):
#             result.append(start_stamp + 3600 * i)
#         # 将unix时间戳转换为“当前时间”格式
#         result = [datetime.datetime.fromtimestamp(stamp) for stamp in result[:]]
#         # result = [date.strftime("%d %m %Y %H:%M:%S") for date in result[:]]
#         result = [date.strftime("%Y%m%d%H") for date in result[:]]
#         return result
# 
#     import datetime, time
# 
# 
#     if not True or not True:
#         print('asdasd')
#     # print(timestampProcess(['2022010110', '20220102010']))



from PyQt5.Qt import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('显示图片的学习')
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        # 从本地读图
        filename = './resources/images/background2.jpg';
        pixmap = QPixmap(filename)  # 按指定路径找到图片

        label = QLabel(self)
        label.setPixmap(pixmap)  # 在label上显示图片


        label.setScaledContents(True) # 让图片自适应大小

        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0,0,0,0)
        v_layout.addWidget(label)
        self.setLayout(v_layout)




if __name__ == '__main__':
    # 测试代码
    import sys
    app = QApplication(sys.argv)
    
    window = Window()
    window.show()


    sys.exit(app.exec())
# 
