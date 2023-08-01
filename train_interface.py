from PyQt5.Qt import *
from resources.train_pane_ui import Ui_Form
from PyQt5 import QtCore
from xml_parse import *
from parameters_form import *


class TrainInterface(QWidget, Ui_Form):
    start_train_btn_signal = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.tmp_csv_save_qw.hide()
        self.test_image_save_qw.hide()
        self.model_cn_dict = readCnName()
        self.initModelForm()
        self.show_test_figure_cb.setEnabled(False)
        # self.signalLink()
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 这条命令设置后会隐藏窗口
        # self.adjustSize()

    def initModelForm(self):
        self.parameter_list = ParameterList()
        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0,0,0,0)
        v_layout.addWidget(self.parameter_list)
        self.parameter_list_qw.setLayout(v_layout)

    def saveTmpCsvBtn(self, checked):
        if checked:
            self.tmp_csv_save_qw.show()
        else:
            self.tmp_csv_save_qw.hide()

    def saveTestFigure(self, checked):
        if checked:
            self.test_image_save_qw.show()
            self.show_test_figure_cb.setEnabled(True)
        else:
            self.test_image_save_qw.hide()
            self.show_test_figure_cb.setEnabled(False)

    def researchMaskPathBtn(self):
        path = QFileDialog.getOpenFileName(self, '范围掩膜影像', default_import_data_dir, '影像数据(*.tif *.tiff)',
                                           '影像数据(*.tif *.tiff)')[0]
        if path != '':
            self.research_space_le.setText(path)

    def importDataPathBtn(self):
        path = QFileDialog.getOpenFileName(self, '导入数据', default_import_data_dir, '数据(*.csv *.xls *.xlsx *.txt)',
                                           '数据(*.csv *.xls *.xlsx *.txt)')[0]
        if path != '':
            self.import_train_data_le.setText(path)

    def exportModelPathBtn(self):
        path = QFileDialog.getSaveFileName(self, '导出模型', default_export_model_dir, '模型二进制文件(*.pkl)', '模型二进制文件(*.pkl)')[
            0]
        if path != '':
            self.export_model_le.setText(path)



    def saveTestFigureBtn(self):
        path = \
        QFileDialog.getSaveFileName(self, '导出模型测试图', default_export_data_dir, '图(*.jpg *.png)', '图(*.jpg *.png)')[0]
        if path != '':
            self.test_figure_save_le.setText(path)



    def saveTmpCsvPathBtn(self):
        path = \
        QFileDialog.getSaveFileName(self, '导出中间表格数据', default_export_data_dir, '类表格数据(*.csv)', '类表格数据(*.csv)')[0]
        if path != '':
            self.tmp_csv_save_le.setText(path)



    # 左边预处理部分
    def yPathImportBtn(self):
        if self.parameter_list.current_model == 'MTL' or self.parameter_list.current_model == 'ST-MTL':
            # 多任务学习
            i = 3
            dir_list = []
            dir = QFileDialog.getExistingDirectory(self, '任务1标签数据文件夹', default_import_data_dir)
            if dir != '':
                dir_list.append(dir)
                dir = QFileDialog.getExistingDirectory(self, '任务2标签数据文件夹', default_import_data_dir)
                if dir != '':
                    dir_list.append(dir)
                    while True:
                        reply = QMessageBox.question(self,
                                                     '提示',
                                                     "是否添加第" + str(i) + "个任务？",
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            dir = QFileDialog.getExistingDirectory(self, '任务' + str(i) + '标签数据文件夹', default_import_data_dir)
                            if dir != '':
                                dir_list.append(dir)
                                i = i + 1
                            else:
                                break
                        else:
                            break
            if len(dir_list) >= 2:
                self.parameter_list.models_map_form_dict[self.parameter_list.current_model].label_line['targetNum_le'].setText(str(len(dir_list)))
                self.y_path_le.setText(str(dir_list))
        else:
        # 单任务学习
            dir = QFileDialog.getExistingDirectory(self, '标签数据文件夹', default_import_data_dir)
            if dir != '':
                self.y_path_le.setText(str([dir]))

    def fastImportBtn(self, item):
        if item.column() == 1: # 这里列应该是1还是2？是1
            dir = QFileDialog.getExistingDirectory(self, '变量影像文件夹', default_import_data_dir)
            if dir != '':
                item.setText(dir)
        else:
            return




    def addVariableBtn(self):
        new_row = self.variable_table_tw.rowCount()
        self.variable_table_tw.insertRow(new_row)
        # print(self.table.columnCount())
        for i in range(self.variable_table_tw.columnCount()):
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.variable_table_tw.setItem(new_row, i, item)
        pass

    def deleteVariableBtn(self):
        if not self.variable_table_tw.selectedItems():
            return
        tmp_set = set()
        for i in self.variable_table_tw.selectedItems():
            tmp_set.add(i.row())
        # print(self.table.currentRow())
        row_remove_list = list(tmp_set)
        row_remove_list.sort()
        tmp_list = [row_remove_list[i]-i for i in range(len(row_remove_list))]
        for i in tmp_list:
            self.variable_table_tw.removeRow(i)

    def checkEnabledStartTrainBtn(self):
        # 后续可以添加更严格的验证器

        # 研究时间暂时不用判断，因为可能直接将文件夹里所有文件都用上
        if self.research_space_le.text() == '':
            return False
        if self.y_path_le.text() == '':
            return False
        if self.random_state_le.text() == '' or self.test_rate_le.text() == '':
            return False
        if self.export_model_le.text() == '':
            return False
        return True

    def startTrain(self):
        # 先判断表单的输入是否完整，否则回一个qmessage信息
        if not self.checkEnabledStartTrainBtn():
            q = QMessageBox.about(self, '提示', '输入参数有误，请改正后提交')
            q.setIcon()
            return
        # 拿好参数
        '''
        {'research_space': '12321312123xxx123123', 
        'research_time': '123xxx', 
        'y_label': []列表
        'save_tmp_csv': {'save_state': 'False', 'save_path': ''}, 
        'x_variables': {'AOD': '123', 'PM': '213'}, 
        'model': 'AdaBoost', 
        'spacetime': '123', 
        'parameters': {'max_depth': '50', 'learning_rate': '0.8'}, 
        'export_model': 'G:\\software_development\\graduation_design\\models\\demo__AdaBoost__trained_model.pkl', 
        'test_rate': '0.1', 
        'random_state': '2', 
        'model_test': {'show_state': 'False', 'save_state': 'False', 'save_path': ''}}
        '''
        para_dict = {}
        para_dict['research_space'] = self.research_space_le.text()
        # 读一下研究时间
        # if self.research_time_le.text() == '':
        #     tmp_time = self.research_time_le.placeholderText().replace('示例：', '')
        # else:
        #     tmp_time = self.research_time_le.text()
        para_dict['research_time'] = self.research_time_le.text().split('-')
        para_dict['y_label'] = self.y_path_le.text()
        para_dict['save_tmp_csv'] = {'save_state':self.tmp_csv_save_cb.isChecked(), 'save_path': self.tmp_csv_save_le.text()}
        tmp_dict = {}
        for i in range(self.variable_table_tw.rowCount()):
            tmp_dict[self.variable_table_tw.item(i,0).text()] = self.variable_table_tw.item(i,1).text()
        para_dict['x_variables'] = tmp_dict
        para_dict['model'] = self.parameter_list.current_model
        # 判断是否调用预处理程序
        model_state_dict = readSpaceTimeState()
        if model_state_dict[self.parameter_list.current_model] == '是':
            para_dict['spacetime'] = '是'
        else:
            para_dict['spacetime'] = '否'
        para_dict['cn_name'] = self.model_cn_dict[para_dict['model']]
        tmp_dict = {}
        # 释放信号到外界，交给外界处理这些信息
        parameter_keys = list(self.parameter_list.models_dict[self.parameter_list.current_model].keys())
        for key in parameter_keys:
            tmp_dict[key] = self.parameter_list.models_map_form_dict[self.parameter_list.current_model].label_line[key+'_le'].text()
        para_dict['parameters'] = tmp_dict
        para_dict['export_model'] = self.export_model_le.text()
        para_dict['test_rate'] = self.test_rate_le.text()
        para_dict['random_state'] = self.random_state_le.text()
        tmp_dict = {}
        # tmp_dict['show_state'] = self.show_test_figure_cb.isChecked()
        tmp_dict['save_state'] = self.save_test_figure_cb.isChecked()
        tmp_dict['save_path'] = self.test_figure_save_le.text()
        para_dict['model_test'] = tmp_dict
        # # 预处理部分
        #     # 判断一下目标值数据是表格数据还是影像数据
        # file_name, file_ext = os.path.splitext(self.y_path_le.text())
        # name = ''
        # # if file_ext == '.tif' or file_ext == '.tiff':
        # #     pass
        # # else:
        # #     pass
        writeTrainXML(para_dict)


        # print(para_dict)
        self.start_train_btn_signal.emit('train')
        pass

if __name__ == '__main__':
    # 测试代码
    import sys

    app = QApplication(sys.argv)

    window = TrainInterface()



    window.show()

    sys.exit(app.exec())