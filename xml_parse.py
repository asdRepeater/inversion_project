# -*- coding: utf-8 -*-
from xml.dom.minidom import parse, Document
import sys
import os
import re



BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
initial_parameters_xml_path = os.path.join(BASE_DIR, 'initial_parameters.xml')
train_xml_path = os.path.join(BASE_DIR, 'train.xml')
predict_xml_path = os.path.join(BASE_DIR, 'predict.xml')
# launch_cost_xml_path = os.path.join(BASE_DIR, 'launch_cost.xml')
recent_browse_xml_path = os.path.join(BASE_DIR, 'recent_browse.xml')
model_info_json_path = os.path.join(BASE_DIR, 'model_info.json')


default_export_model_dir = os.path.join(BASE_DIR, 'models\\')
default_import_data_dir = os.path.join(BASE_DIR, 'import_data\\')
default_export_data_dir = os.path.join(BASE_DIR, 'export_data\\')
default_export_tif_dir = os.path.join(default_export_data_dir, 'tif\\')
default_tmp_workspace_dir = os.path.join(BASE_DIR, 'tmp_workspace\\')

default_machine_learning_exe_path = os.path.join(BASE_DIR, 'machine_learning_v3.0.exe')





# print('哈哈哈   ' + os.path.realpath(sys.argv[0]))
# print(default_export_model_dir, default_import_data_dir)




def readFileName(path):
	dirStr, ext = os.path.splitext(path)
	# file = dirStr.split("\\", "/")[-1]
	file = re.split(r'[\\/]', dirStr)[-1]
	return file


def initDir():
	if not os.path.exists(default_export_model_dir):
		os.makedirs(default_export_model_dir)
	if not os.path.exists(default_import_data_dir):
		os.makedirs(default_import_data_dir)
	if not os.path.exists(default_export_data_dir):
		os.makedirs(default_export_data_dir)
	if not os.path.exists(default_tmp_workspace_dir):
		os.makedirs(default_tmp_workspace_dir)
	if not os.path.exists(default_export_tif_dir):
		os.makedirs(default_export_tif_dir)

def readInitXML():
	'''
	读取xml文件
	:param xml_path: xml文件路径
	:return:
		返回一个包含各模型及参数的二层字典，例如：
		{'model1': {"parameter1":value1, "parameter2":value2},
		'model2': {"parameter1":value1, "parameter2":value2},
		'model3':{},...]
	'''
	domTree = parse(initial_parameters_xml_path)
	# 文档根元素
	rootNode = domTree.documentElement

	model_dict = {}


	# print(rootNode.nodeName)
	# 所有model
	models = rootNode.getElementsByTagName("model")
	# print("****所有模型信息****")
	for model in models:
		tmp_dict = {}
		# print("ID:", model.getAttribute("ID"))
		# 所有参数信息
		parameters = model.getElementsByTagName("parameter")
		for parameter in parameters:
			# print(parameter.getAttribute("name") + ": " + parameter.childNodes[0].data)
			tmp_dict[parameter.getAttribute("name")] = parameter.childNodes[0].data
		model_dict[model.getAttribute("ID")] = tmp_dict

	# print(model_dict)
	return model_dict


def readCnName():
	domTree = parse(initial_parameters_xml_path)
	# 文档根元素
	rootNode = domTree.documentElement
	model_dict = {}
	# 所有model
	models = rootNode.getElementsByTagName("model")
	# print("****所有模型信息****")
	for model in models:
		model_dict[model.getAttribute("ID")] = model.getAttribute("cn_name")
	return model_dict

def readSpaceTimeState():
	domTree = parse(initial_parameters_xml_path)
	# 文档根元素
	rootNode = domTree.documentElement
	model_dict = {}
	# 所有model
	models = rootNode.getElementsByTagName("model")
	# print("****所有模型信息****")
	for model in models:
		model_dict[model.getAttribute("ID")] = model.getAttribute("spacetime")
	return model_dict

# def writeXML(xml_path, model_dict):
# 	'''
# 	添加算法模型
# 	:param xml_path: xml文件路径
# 	:param model_dict: 模型字典——{"ID":model, "parameter_name_1":value1, "parameter_name_2":value2}
# 	:return:
# 	'''
# 	model = model_dict['ID']
#
#
#
# 	domTree = parse(xml_path)
# 	# 文档根元素
# 	rootNode = domTree.documentElement
# 	# 新建一个model节点
# 	model_node = domTree.createElement("model")
# 	model_node.setAttribute("ID", model_dict['ID'])
#
# 	# 创建parameter节点,并设置参数值
# 	for i in range(1, len(model_dict.keys())):
# 		keys = list(model_dict.keys())
# 		parameter_node = domTree.createElement("parameter")
# 		parameter_node.setAttribute("name", str(keys[i]))
# 		parameter_text_value = domTree.createTextNode(str(model_dict[keys[i]]))
# 		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
# 		model_node.appendChild(parameter_node)
#
# 	rootNode.appendChild(model_node)
#
# 	with open('./new_model_parameters.xml', 'w') as f:
# 		# 缩进 - 换行 - 编码
# 		domTree.writexml(f, addindent='	', newl='\n', encoding='utf-8')
def readTrainXML():
	'''
	读取xml文件
	:param xml_path: xml文件路径
	:return:
		返回一个包含（模型名称，模型参数字典，输入数据路径，输出路径，测试比率，随机数种子，模型测试效果图表字典）的字典。例如：
	<research_space></research_space>
	<research_time></research_time>
	<y_label></y_label>
	<x_variables>
	</x_variables>
	<save_tmp_csv save_state="True"></save_tmp_csv>
	<model ID="AdaBoost">
		<parameter name="max_depth">50</parameter>
		<parameter name="learning_rate">0.8</parameter>
	</model>
	<export_model_path>G:\software_development\graduation_design\models\demo__AdaBoost__trained_model.pkl</export_model_path>
	<test_rate>0.1</test_rate>
	<random_state>2</random_state>
	<model_test save_state="False" show_state="False"></model_test>
	'''
	domTree = parse(train_xml_path)
	# 文档根元素
	rootNode = domTree.documentElement

	dict = {}
	research_space = rootNode.getElementsByTagName("research_space")[0]
	dict['research_space'] = research_space.childNodes[0].data
	research_time = rootNode.getElementsByTagName("research_time")[0]
	dict['research_time'] = research_time.childNodes[0].data
	y_label = rootNode.getElementsByTagName("y_label")[0]
	dict['y_label'] = y_label.childNodes[0].data

	tmp_dict = {}
	save_tmp_csv = rootNode.getElementsByTagName('save_tmp_csv')[0]
	save_state = save_tmp_csv.getAttribute('save_state')
	tmp_dict['save_state'] = save_state
	if save_state == 'True':
		tmp_dict['save_path'] = save_tmp_csv.childNodes[0].data
	else:
		tmp_dict['save_path'] = ''
	dict['save_tmp_csv'] = tmp_dict

	x_variables = rootNode.getElementsByTagName("x_variables")[0]
	tmp_dict = {}
	parameters = x_variables.getElementsByTagName("var")
	for parameter in parameters:
		tmp_dict[parameter.getAttribute("name")] = parameter.childNodes[0].data
	dict['x_variables'] = tmp_dict
	# 所有model
	model = rootNode.getElementsByTagName("model")[0]
	dict['model'] = model.getAttribute("ID")
	dict['spacetime'] = model.getAttribute("spacetime")
	dict['cn_name'] = model.getAttribute('cn_name')
	tmp_dict = {}
	# 所有参数信息
	parameters = model.getElementsByTagName("parameter")
	for parameter in parameters:
		tmp_dict[parameter.getAttribute("name")] = parameter.childNodes[0].data
	dict['parameters'] = tmp_dict

	export_model = rootNode.getElementsByTagName('export_model')[0]
	dict['export_model'] = export_model.childNodes[0].data

	test_rate = rootNode.getElementsByTagName('test_rate')[0]
	dict['test_rate'] = test_rate.childNodes[0].data

	random_state = rootNode.getElementsByTagName('random_state')[0]
	dict['random_state'] = random_state.childNodes[0].data

	tmp_dict = {}
	model_test = rootNode.getElementsByTagName('model_test')[0]
	# show_state = model_test.getAttribute('show_state')
	save_state = model_test.getAttribute('save_state')
	# tmp_dict['show_state'] = show_state
	tmp_dict['save_state'] = save_state
	if save_state == 'True':
		tmp_dict['save_path'] = model_test.childNodes[0].data
	else:
		tmp_dict['save_path'] = ''
	dict['model_test'] = tmp_dict

	# print(dict)
	return dict

def writeTrainXML(dict):
	'''
	写入xml
	:param 	写入一个包含（模型名称，模型参数字典，输入数据路径，输出路径，测试比率，随机数种子，模型测试效果图表字典）的字典。例如：
		{'model':model_name,
		'parameters': {"parameter1":value1, "parameter2":value2},
		'data_path':'./...',
		'export_model_path':'./...',
		'test_rate':value,
		'random_state':value,
		'model_test_figure': {'show_state':boolean, 'save_state':boolean, 'save_path': value}}
	:return:
	'''

	keys = list(dict.keys())

	# domTree = parse(xml_path)
	domTree = Document()
	# imp = getDOMImplementation()
	# domTree = imp.createDocument()

	# 文档根元素
	rootNode = domTree.createElement('root')
	# 创建每一个节点
	research_space = domTree.createElement('research_space')
	node_value = domTree.createTextNode(str(dict['research_space']))
	research_space.appendChild(node_value)
	rootNode.appendChild(research_space)

	research_time = domTree.createElement('research_time')
	node_value = domTree.createTextNode(str(dict['research_time']))
	research_time.appendChild(node_value)
	rootNode.appendChild(research_time)

	y_label = domTree.createElement('y_label')
	node_value = domTree.createTextNode(str(dict['y_label']))
	y_label.appendChild(node_value)
	rootNode.appendChild(y_label)

	# < save_tmp_csv save_state = "True" > < / save_tmp_csv >
	save_tmp_csv = domTree.createElement('save_tmp_csv')
	save_tmp_csv.setAttribute('save_state', str(dict['save_tmp_csv']['save_state']))
	save_tmp_csv_text_value = domTree.createTextNode(str(dict['save_tmp_csv']['save_path']))
	save_tmp_csv.appendChild(save_tmp_csv_text_value)
	rootNode.appendChild(save_tmp_csv)

	x_variables = domTree.createElement('x_variables')
	var_dict = dict['x_variables']
	for i in range(0, len(var_dict)):
		var_keys = list(var_dict.keys())
		# print(para_keys)
		parameter_node = domTree.createElement("var")
		parameter_node.setAttribute("name", str(var_keys[i]))
		parameter_text_value = domTree.createTextNode(str(var_dict[var_keys[i]]))
		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
		x_variables.appendChild(parameter_node)
	rootNode.appendChild(x_variables)

	# 新建一个model节点
	model_node = domTree.createElement("model")
	model_node.setAttribute("ID", dict['model'])
	model_node.setAttribute("spacetime", dict['spacetime'])
	model_node.setAttribute("cn_name", dict['cn_name'])
	# 创建parameter节点,并设置参数值
	para_dict = dict['parameters']
	for i in range(0, len(para_dict)):
		para_keys = list(para_dict.keys())
		# print(para_keys)
		parameter_node = domTree.createElement("parameter")
		parameter_node.setAttribute("name", str(para_keys[i]))
		parameter_text_value = domTree.createTextNode(str(para_dict[para_keys[i]]))
		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
		model_node.appendChild(parameter_node)
	rootNode.appendChild(model_node)

	# 创建export节点
	export_node = domTree.createElement('export_model')
	export_node_text_value = domTree.createTextNode(str(dict['export_model']))
	export_node.appendChild(export_node_text_value)
	rootNode.appendChild(export_node)

	# 创建test_rate节点
	test_rate_node = domTree.createElement('test_rate')
	test_rate_text_value = domTree.createTextNode(str(dict['test_rate']))
	test_rate_node.appendChild(test_rate_text_value)
	rootNode.appendChild(test_rate_node)

	# 创建random_state节点
	random_state_node = domTree.createElement('random_state')
	random_state_text_value = domTree.createTextNode(str(dict['random_state']))
	random_state_node.appendChild(random_state_text_value)
	rootNode.appendChild(random_state_node)

	# 创建model_test_figure节点
	model_test_figure_node = domTree.createElement('model_test')
	# model_test_figure_node.setAttribute('show_state', str(dict['model_test']['show_state']))
	model_test_figure_node.setAttribute('save_state', str(dict['model_test']['save_state']))
	model_test_figure_text_value = domTree.createTextNode(str(dict['model_test']['save_path']))
	model_test_figure_node.appendChild(model_test_figure_text_value)
	rootNode.appendChild(model_test_figure_node)
	domTree.appendChild(rootNode)

	with open(train_xml_path, mode='w', encoding="utf-8") as f:
		# 缩进 - 换行 - 编码
		domTree.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')

# def updateXML(xml_path, model_dict):
# 	'''
# 	更改模型参数
# 	:param xml_path: xml文件路径
# 	:param model_dict: 模型字典——{"ID":model, "parameter_name_1":value1, "parameter_name_2":value2}
# 	:return:
# 	'''
# 	domTree = parse(xml_path)
# 	# 文档根元素
# 	rootNode = domTree.documentElement
#
# 	# 新节点
# 	new_model = domTree.createElement("model")
# 	new_model.setAttribute("ID", model_dict['ID'])
#
# 	# 创建parameter节点,并设置参数值
# 	for i in range(1, len(model_dict.keys())):
# 		keys = list(model_dict.keys())
# 		parameter_node = domTree.createElement("parameter")
# 		parameter_node.setAttribute("name", str(keys[i]))
# 		parameter_text_value = domTree.createTextNode(str(model_dict[keys[i]]))
# 		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
# 		new_model.appendChild(parameter_node)
#
# 	models = rootNode.getElementsByTagName("model")
# 	for model in models:
# 		if model.getAttribute('ID') == model_dict['ID']:
# 			# 获取到parameter节点
# 			rootNode.replaceChild(new_model, model)
# 			break
# 	else:
# 		print('没有找到该算法模型')
#
# 	with open(xml_path, 'w') as f:
# 		# 缩进 - 换行 - 编码
# 		domTree.writexml(f, addindent='	', newl='\n', encoding='utf-8')

def readPredictXml():

	domTree = parse(predict_xml_path)
	rootNode = domTree.documentElement
	dict = {}
	# 所有model
	predict_space_node = rootNode.getElementsByTagName("predict_space")[0]
	dict['predict_space'] = predict_space_node.childNodes[0].data

	predict_time_node = rootNode.getElementsByTagName("predict_time")[0]
	dict['predict_time'] = predict_time_node.childNodes[0].data

	model_path_node = rootNode.getElementsByTagName("model")[0]
	dict['model'] = model_path_node.childNodes[0].data

	tmp_dict = {}
	save_tmp_csv = rootNode.getElementsByTagName('save_tmp_csv')[0]
	save_state = save_tmp_csv.getAttribute('save_state')
	tmp_dict['save_state'] = save_state
	if save_state == 'True':
		tmp_dict['save_path'] = save_tmp_csv.childNodes[0].data
	else:
		tmp_dict['save_path'] = ''
	dict['save_tmp_csv'] = tmp_dict

	x_variables = rootNode.getElementsByTagName("x_variables")[0]
	tmp_dict = {}
	parameters = x_variables.getElementsByTagName("var")
	for parameter in parameters:
		tmp_dict[parameter.getAttribute("name")] = parameter.childNodes[0].data
	dict['x_variables'] = tmp_dict


	predict_data_path_node = rootNode.getElementsByTagName("export_type")[0]
	dict['export_type'] = predict_data_path_node.childNodes[0].data
	export_result_path_node = rootNode.getElementsByTagName("export_result")[0]
	dict['export_result'] = export_result_path_node.childNodes[0].data
	# print(dict)
	return dict


def writePredictXml(dict):
	domTree = Document()
	rootNode = domTree.createElement('root')

	tmp_node = domTree.createElement('predict_space')
	tmp_node_text_value = domTree.createTextNode(str(dict['predict_space']))
	tmp_node.appendChild(tmp_node_text_value)
	rootNode.appendChild(tmp_node)

	tmp_node = domTree.createElement('predict_time')
	tmp_node_text_value = domTree.createTextNode(str(dict['predict_time']))
	tmp_node.appendChild(tmp_node_text_value)
	rootNode.appendChild(tmp_node)

	tmp_node = domTree.createElement('model')
	tmp_node_text_value = domTree.createTextNode(str(dict['model']))
	tmp_node.appendChild(tmp_node_text_value)
	rootNode.appendChild(tmp_node)

	x_variables = domTree.createElement('x_variables')
	var_dict = dict['x_variables']
	for i in range(0, len(var_dict)):
		var_keys = list(var_dict.keys())
		# print(para_keys)
		parameter_node = domTree.createElement("var")
		parameter_node.setAttribute("name", str(var_keys[i]))
		parameter_text_value = domTree.createTextNode(str(var_dict[var_keys[i]]))
		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
		x_variables.appendChild(parameter_node)
	rootNode.appendChild(x_variables)
	# < save_tmp_csv save_state = "True" > < / save_tmp_csv >
	save_tmp_csv = domTree.createElement('save_tmp_csv')
	save_tmp_csv.setAttribute('save_state', str(dict['save_tmp_csv']['save_state']))
	save_tmp_csv_text_value = domTree.createTextNode(str(dict['save_tmp_csv']['save_path']))
	save_tmp_csv.appendChild(save_tmp_csv_text_value)
	rootNode.appendChild(save_tmp_csv)

	tmp_node = domTree.createElement('export_type')
	tmp_node_text_value = domTree.createTextNode(str(dict['export_type']))
	tmp_node.appendChild(tmp_node_text_value)
	rootNode.appendChild(tmp_node)

	tmp_node = domTree.createElement('export_result')
	tmp_node_text_value = domTree.createTextNode(str(dict['export_result']))
	tmp_node.appendChild(tmp_node_text_value)
	rootNode.appendChild(tmp_node)

	domTree.appendChild(rootNode)

	with open(predict_xml_path, mode='w', encoding="utf-8") as f:
		# 缩进 - 换行 - 编码
		domTree.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')


def readRecentBrowseXml():
	domTree = parse(recent_browse_xml_path)
	rootNode = domTree.documentElement
	dict = {}
	# 所有model

	train = rootNode.getElementsByTagName("train")[0]
	train_models = train.getElementsByTagName('model')
	for train_model in train_models:
		key = train_model.getAttribute('seq')
		dict[int(key)] = train_model.childNodes[0].data

	train_sorted = sorted(dict.items(),key=lambda x: x[0], reverse=False)
	train_list = [i[1] for i in train_sorted]
	dict = {}
	predict = rootNode.getElementsByTagName("predict")[0]
	predict_models = predict.getElementsByTagName('model')
	for predict_model in predict_models:
		key = predict_model.getAttribute('seq')
		dict[key] = predict_model.childNodes[0].data
	predict_sorted = sorted(dict.items(),key=lambda x: x[0], reverse=False)
	predict_list = [i[1] for i in predict_sorted]
	return train_list, predict_list

def writeRecentBrowseXml(train_list, predict_list):

	models = train_list
	domTree = Document()
	# 文档根元素
	rootNode = domTree.createElement('root')
	# 创建每一个节点
	train = domTree.createElement('train')
	for i in range(len(models)):
		parameter_node = domTree.createElement("model")
		parameter_node.setAttribute("seq", str(i))
		parameter_text_value = domTree.createTextNode(str(models[i]))
		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
		train.appendChild(parameter_node)
	rootNode.appendChild(train)


	models = predict_list
	predict = domTree.createElement('predict')
	for i in range(len(models)):
		parameter_node = domTree.createElement("model")
		parameter_node.setAttribute("seq", str(i))
		parameter_text_value = domTree.createTextNode(str(models[i]))
		parameter_node.appendChild(parameter_text_value)  # 把文本节点挂到name_node节点
		predict.appendChild(parameter_node)
	rootNode.appendChild(predict)
	domTree.appendChild(rootNode)
	with open(recent_browse_xml_path, mode='w', encoding="utf-8") as f:
		# 缩进 - 换行 - 编码
		domTree.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')
def updateRecentBrowseXml(type, name):
	# 完成训练或者完成预测时才更新， 因为训练时除训练算法会变化，生成的模型也会添加进去（不用不用，到时候在调用一次即可）
	# 模型没有
	train_list, predict_list = readRecentBrowseXml()
	domTree = parse(recent_browse_xml_path)
	rootNode = domTree.documentElement
	# 修改
	if type == 'train':
		for i in range(len(train_list)):
			if name == train_list[i]:
				train_list.pop(i)
				train_list.insert(0, name)
				# 还要修改predict_list
				break
	elif type == 'predict':
		for i in range(len(predict_list)):
			if name == predict_list[i]:
				predict_list.pop(i)
				predict_list.insert(0, name)
				break
	# 重新写入
	writeRecentBrowseXml(train_list, predict_list)


def initRecentBrowseXml():
	if not os.path.exists(recent_browse_xml_path) or os.path.getsize(recent_browse_xml_path) == 0:
		dict = readCnName()
		train_list = [value + '(' + key + ')' for key, value in dict.items()]
		predict_list = [i[:-4] for i in os.listdir(default_export_model_dir)] # 不要PKL
		writeRecentBrowseXml(train_list, predict_list)


# def readCostXml():
# 	domTree = parse(launch_cost_xml_path)
# 	rootNode = domTree.documentElement
# 	cost = rootNode.getElementsByTagName('launch_cost')[0].childNodes[0].data
# 	return cost

# def writeCostXml(cost):
#
# 	domTree = Document()
#
# 	rootNode = domTree.createElement('root')
# 	tmp_node = domTree.createElement('launch_cost')
# 	tmp_node_text_value = domTree.createTextNode(str(cost))
# 	tmp_node.appendChild(tmp_node_text_value)
# 	rootNode.appendChild(tmp_node)
#
# 	domTree.appendChild(rootNode)
#
# 	with open(launch_cost_xml_path, mode='w', encoding="utf-8") as f:
# 		# 缩进 - 换行 - 编码
# 		domTree.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')

if __name__ == '__main__':
	# model_list = readXML("./initial_parameters.xml")
	# writeXML(xmlpath, {'ID':'AdaBoost', 'max_depth': 50, 'learning_rate': 0.8})
	# updateXML(xmlpath, {'ID':'AdaBoost', 'max_depth': 30, 'learning_rate': 1})

	# writeTrainXML({'model':'RF',
	# 			   'parameters':{'asdasd':'asdasd', '123':'mnxcmn'},
	# 			   'data_path':'./asdasdasd',
	# 			   'export_model_path':'123131',
	# 			   'test_rate':0.1,
	# 			   'random_state':2,
	# 			   'model_test_figure':{'show_state':'True', 'save_state':'False', 'save_path': 'asdasd'}})

	# print(readTrainXML())

	# readPredictXml()
	# writePredictXml({'predict_data_path': 'leishimin', 'predict_model_path': 'asdasdasd', 'export_result_path': '123123123'})

	# print(initial_parameters_xml_path)
	# print(train_xml_path)
	# print(default_export_model_dir)

	# print(readFileName('C:/asda/asdasd/leishimin.jpg'))

	#
	# # writeCostXml(1231123123)
	# print(readCostXml())
	#
	# print(readCnName())
	# print(readSpaceTimeState())



	# writeTrainXML(dict)

	# writeTrainXML(readTrainXML())

	# print(readTrainXML())

	# writeRecentBrowseXml()
	# print(readRecentBrowseXml())

	# updateRecentBrowseXml('train', 'RF|随机森林')

	print(readPredictXml())

	writePredictXml(readPredictXml())
