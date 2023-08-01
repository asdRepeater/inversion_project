import os

from PyQt5.Qt import *
from resources.predict_pane_ui import Ui_Form
from PyQt5 import QtCore
from xml_parse import *
from parameters_form import ParameterForm
import json

class PredictInterface(QWidget, Ui_Form):
    start_predict_btn_signal = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 这条命令设置后会隐藏窗口
        self.current_model = ''
        self.model_info_dict = {}
        self.result_type = ''
        self.set_up()
        self.mode_cn_dict = readCnName()


    def setModelInfo(self):
        with open(model_info_json_path, 'r', encoding='utf-8') as fp:
            self.model_info_dict = json.load(fp)
        info = self.model_info_dict[self.current_model]
        # self.model_name_l.buddy().append(info['model_name'])
        # self.model_algorithm_l.buddy().append(info['model_algorithm'])
        # self.model_spacetime_l.buddy().append(info['model_spacetime'])
        # self.model_parameters_l.buddy().append(info['model_parameters'])
        # self.model_research_range_l.buddy().append(info['model_research_range'])
        # self.model_variable_num_l.buddy().append(info['model_var'])
        # self.model_accuracy_l.buddy().append(info['model_accuracy'])
        # tmp_str = '"<table width="100%"><tr><td style="vertical-align: middle;">' + info['model_name'] + '</td></tr></table>"'
        self.model_name_l.buddy().setText(info['model_name'])
        self.model_algorithm_l.buddy().setText(self.mode_cn_dict[info['model_algorithm']] + '(' + info['model_algorithm'] + ')')
        self.model_spacetime_l.buddy().setText(info['model_spacetime'])
        para_info = ''
        for key, value in info['model_parameters'].items():
            para_info += str(key) + ": " + str(value) + "\n"
        para_info = para_info[:-1]
        self.model_parameters_l.buddy().setText(para_info)
        range_info = "空间: " + info['model_research_range']['空间'] + "\n" + "时间: " + info['model_research_range']['时间'][0] + "~" + info['model_research_range']['时间'][1]
        self.model_research_range_l.buddy().setText(range_info)
        var_info = ''
        for i in info['model_var']:
            var_info += i + ' '
        var_info = var_info[:-1]
        self.model_variable_num_l.buddy().setText(var_info)
        accuracy_info = ''
        for i in info['model_accuracy']:
            accuracy_info += i + '\n'
        accuracy_info = accuracy_info[:-1]
        self.model_variable_num_l.buddy().setText(var_info)
        self.model_accuracy_l.buddy().setText(accuracy_info)

    def set_up(self):
        # 读取json模型内容
        with open(model_info_json_path, 'r', encoding='utf-8') as fp:
            self.model_info_dict = json.load(fp)

        self.tmp_csv_save_qw.hide()
        self.result_type = 'tif'
        self.tif_rb.setChecked(True)
        # self.result_save_qw.hide()

        for i in self.left_qw.findChildren(QTextBrowser):
            i.setStyleSheet("QTextBrowser{font-weight: bold;}")
            # i.setAlignment(Qt.AlignCenter)
            # i.adjustSize()
            # print(i.height())



    def enabledPredictBtn(self):
        if self.import_predict_data_le.text() != '' and self.model_select_le.text() != '' and self.export_result_le.text() != '':
            self.start_predict_btn.setEnabled(True)
        else:
            self.start_predict_btn.setEnabled(False)

    def predictSpacePathBtn(self):
        path = QFileDialog.getOpenFileName(self, '推理空间范围', default_import_data_dir, '参考影像(*.tif)', '参考影像(*.tif)')[0]
        if path != '':
            self.predict_space_le.setText(path)
        pass

    def resultBtn(self):
        if self.result_type == 'tif':
            path = QFileDialog.getExistingDirectory(self, '导出预测结果', default_export_data_dir)
        else:
            str = '预测结果(*.' + self.result_type + ')'
            path = QFileDialog.getSaveFileName(self, '导出预测结果', default_export_data_dir, str, str)[0]
        self.result_save_le.setText(path)
        pass


    def saveResultRb(self, checked):
        if checked:
            self.result_save_qw.show()
            if self.sender() is self.tif_rb:
                self.result_type = 'tif'
                self.result_save_le.setPlaceholderText('tif输出文件夹路径')
                pass
            elif self.sender() is self.single_csv_rb:
                self.result_type = 'csv'
                self.result_save_le.setPlaceholderText('')
                pass
            elif self.sender() is self.concat_csv_rb:
                self.result_type = 'csv'
                self.result_save_le.setPlaceholderText('')
                pass
    # def predictDataBtn(self):
    #     path = QFileDialog.getOpenFileName(self, '导入预测数据', default_import_data_dir, '预测数据(*.csv *.xls *.xlsx *.txt)',
    #                                        '预测数据(*.csv *.xls *.xlsx *.txt)')[0]
    #     self.import_predict_data_le.setText(path)
    #     pass

    # def modelSelectionBtn(self):
    #     path = QFileDialog.getOpenFileName(self, '选择预测模型', default_export_model_dir, '预测模型(*.pkl)',
    #                                        '预测模型(*.pkl)')[0]
    #     self.model_select_le.setText(path)
    #     pass

    def saveTmpCsvBtn(self, checked):
        if checked:
            self.tmp_csv_save_qw.show()
        else:
            self.tmp_csv_save_qw.hide()

    def saveTmpCsvPathBtn(self):
        path = \
        QFileDialog.getSaveFileName(self, '导出中间表格数据', default_export_data_dir, '类表格数据(*.csv)', '类表格数据(*.csv)')[0]
        if path != '':
            self.tmp_csv_save_le.setText(path)

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

    def checkEnabledStartPredictBtn(self):
        if self.result_save_le.text != '':
            return True
        else:
            return False

    def startPredict(self):
        # 先判断表单的输入是否完整，否则回一个qmessage信息
        if not self.checkEnabledStartPredictBtn():
            q = QMessageBox.about(self, '提示', '输入参数有误，请改正后提交')
            q.setIcon()
            return
        # 拿好参数
        '''
        {
        predict_space:
        predict_time:
        'model':path
        'x_variables': {'AOD': '123', 'PM': '213'}, 
        'save_tmp_csv': {'save_state': 'False', 'save_path': ''}, 
        'export_type': 'single_csv'/'concat_csv'/'tif'
        'export_result': 'G:\\software_development\\graduation_design\\models\\demo__AdaBoost__trained_model.pkl', 
        '''
        para_dict = {}
        para_dict['predict_space'] = self.predict_space_le.text()
        para_dict['predict_time'] = self.predict_time_le.text().split('-')
        para_dict['model'] = os.path.join(default_export_model_dir, self.current_model + '.pkl')
        tmp_dict = {}
        for i in range(self.variable_table_tw.rowCount()):
            tmp_dict[self.variable_table_tw.item(i, 0).text()] = self.variable_table_tw.item(i, 1).text()
        para_dict['x_variables'] = tmp_dict
        export_type = ''
        if self.single_csv_rb.isChecked():
            export_type = 'single_csv'
        elif self.concat_csv_rb.isChecked():
            export_type = 'concat_csv'
        elif self.tif_rb.isChecked():
            export_type = 'tif'
        para_dict['save_tmp_csv'] = {'save_state':self.tmp_csv_save_cb.isChecked(), 'save_path': self.tmp_csv_save_le.text()}
        para_dict['export_type'] = export_type
        para_dict['export_result'] = self.result_save_le.text()

        writePredictXml(para_dict)
        self.start_predict_btn_signal.emit('predict')

        pass
if __name__ == '__main__':
    # 测试代码
    import sys
    app = QApplication(sys.argv)

    window = PredictInterface()
    window.show()

    sys.exit(app.exec())