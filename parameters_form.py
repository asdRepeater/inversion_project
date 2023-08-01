from PyQt5.Qt import *
from xml_parse import readInitXML


class ParameterForm(QWidget):
    def __init__(self, *args, model={}):
        '''

        :param args:
        :param model: 关键字参数：模型以及模型参数所构成的一个键值对字典
        '''
        super().__init__(*args)
        self.label_line = {}
        # self.setMinimumSize(350, 50)
        self.setup_ui(model)
        # self.adjustSize()

    def setup_ui(self, model):
        parameters = list(model.values())[0]
        keys = list(parameters.keys())
        length = len(parameters)
        # 这里应该搞一个表单布局
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.form.setSpacing(10)
        self.form.setContentsMargins(0, 0, 0, 0)

        for i in range(0, length):
            label = QLabel(self)
            label.setText(keys[i])
            label.setFixedHeight(50)
            # label.move(0, 50 * i)
            # label.adjustSize()
            le = QLineEdit(self)
            le.setFixedHeight(50)
            le.setText(parameters[keys[i]])
            self.form.addRow(label, le)
            # if max_len < label.width():
            #     max_len = label.width()
            self.label_line[keys[i]+'_label'] = label
            self.label_line[keys[i] + '_le'] = le


class ParameterList(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.models_dict = readInitXML()
        self.models_name = list(self.models_dict.keys())
        self.models_map_form_dict = {}
        self.current_model = ''
        pass
        self.setup_ui(self.models_dict)
        self.special()

    def setup_ui(self, models_dict):
        '''
        初始化参数列表
        :param models:是个字典，models={模型名称1：{参数1：值，参数2：值，...}，模型名称2：{参数1：值，参数2：值，...}}
        :return:
        '''
        # 给父对象搞一个布局
        v_layout = QVBoxLayout()
        v_layout.setSpacing(10)
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)
        self.v_layout = v_layout
        # 添加参数表单类
        for model, parameter in models_dict.items():
            tmp = {}
            tmp[model] = parameter
            self.models_map_form_dict[model] = ParameterForm(model=tmp)
            self.models_map_form_dict[model].hide()
            v_layout.addWidget(self.models_map_form_dict[model])

        # 添加重置按钮（添加到这里比较合理，因为与参数关联性较强）

        self.reset_btn = QPushButton('重置为默认参数')
        v_layout.addWidget(self.reset_btn)
        self.reset_btn.clicked.connect(self.resetBtn)
    # 槽函数
    def resetBtn(self):
        if self.current_model != '':
            parameters = self.models_dict[self.current_model]
            keys = list(parameters.keys())
            for i in range(0, len(keys)):
                self.models_map_form_dict[self.current_model].label_line[keys[i] + '_le'].setText(parameters[keys[i]])

    # 在外面调用的函数
    def showForm(self, model_name):
        if self.current_model != '':
            self.models_map_form_dict[self.current_model].hide()
        self.current_model = model_name
        self.models_map_form_dict[model_name].show()
        self.adjustSize()
        self.parent().adjustSize()

    def special(self):
        try:
            self.models_map_form_dict['MTL'].label_line['targetNum_le'].setEnabled(False)
            self.models_map_form_dict['ST-MTL'].label_line['targetNum_le'].setEnabled(False)
        except:
            pass

if __name__ == '__main__':
    # 测试代码
    import sys
    import time
    app = QApplication(sys.argv)

    # form = ParameterForm(model={'AdBoost':{'asdasd':'132312','asdasdasdasd':'asdasdasdasd'}})
    #
    # print(form.height())
    # form.show()
    i = 0
    def change():
        global i
        length = len(form.models_name)
        form.showForm(form.models_name[i])
        i = (i + 1) % length
        # window.adjustSize()

    form = ParameterList()


    window = QWidget()

    # window.setFixedWidth(100)

    btn = QPushButton()
    v_layout = QVBoxLayout()
    v_layout.addWidget(btn)
    v_layout.addWidget(form)

    window.setLayout(v_layout)
    window.show()

    btn.clicked.connect(change)

    sys.exit(app.exec())