import glob
import env as env
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import numpy as np
#from openpyxl import Workbook
#import xlwt

### file analyzing

def countingSpecie(xmlFile):
	species_list = []
	xmlTree = ET.parse(xmlFile)
	labels_list = {}
	root = xmlTree.getroot()

	for member in root.findall('object'):
		specie_name = member.find('name').text
		species_list.append(specie_name)

	# label mapping
	for specie_id, specie_name in env.LABEL_MAP.items():
		labels_list[specie_name] = species_list.count(specie_name) 

	return labels_list

### local viewing

def getRawData():
	local_result = {}
	for folder in ['train','eval']:
		labelsList = glob.glob(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + folder + '/' + '*' + env.BASE_TYPE.get('LABEL_EXTENSION'))
		local_result[folder] = {}
		for index in range(len(labelsList)):
			local_result[folder][labelsList[index].split('/')[-1]] = {}

		for key,value in local_result.items():
			local_result[key] = {}
			for subKey,subValue in value.items():
				local_result[key][subKey] = countingSpecie(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + key + '/' + subKey)
	return local_result

### global analyzing

def getGlobalData():
	global_result = {}
	result = getRawData()
	
	for mode,data in result.items():
		global_result[mode] = {}
		for specie_id, specie_name in env.LABEL_MAP.items():
			global_result[mode][specie_name] = sum(d[specie_name] for d in data.values() if d)
	return global_result

# global visualzing by chart ---> bar chart
def barChartVisualizing():
	_bar = np.arange(len(env.LABEL_MAP))		# define how many bar 		### ---> fix here
	
	global_data = getGlobalData()
	
	global_data_in_list = list()
	global_mode = list()

	for mode, data in global_data.items():
		global_data_in_list.append(tuple(data.values()))
		global_mode.append(mode)

	x_val = list(env.LABEL_MAP.keys())

	for _k in range(len(global_mode)):
		ax = plt.subplot()
		for j in range(len(x_val)):
			ax.bar(x_val[j], global_data_in_list[_k][j], width=0.8, bottom=0.0, align='center', color=env.CHART_COLOR[x_val[j]][1], alpha=1, label=env.CHART_COLOR[x_val[j]][0])
	
		for k, v in enumerate(global_data_in_list[_k]):
			ax.text(k+1,v,str(v),color='black',ha='center', fontweight='bold', fontsize=15)
	
		ax.set_xticks(x_val)
		ax.set_xticklabels([env.CHART_COLOR[i][0] for i in x_val])
		plt.xlabel('Specie', fontsize=18)
		plt.ylabel('Specie number', fontsize=18)
		plt.title('Number of specie of ' + global_mode[_k] + ' process', fontweight='bold', fontsize=18)
		ax.legend(title='Specie',fontsize=14)
		plt.show()

# global visualizing by chart ---> pie chart
def pieChartVisualizing():
	pie_data = getGlobalData()
	pie_data_in_list = list()
	pie_mode = list()

	for mode, data in pie_data.items():
		pie_data_in_list.append(data.values())		# [(tuple),(tuple)]
		pie_mode.append(mode)						# pie_mode is "train" or "eval"

	for _mode in range(len(pie_mode)):
		fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

		wedges, texts, autotexts = ax.pie(pie_data_in_list[_mode], wedgeprops=dict(width=0.5), startangle=20, colors=env.getColorList(), autopct='%1.1f%%')

		bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
		kw = dict(arrowprops=dict(arrowstyle="-"),bbox=bbox_props, zorder=0, va="center")

		for i, p in enumerate(wedges):
			ang = (p.theta2 - p.theta1)/2. + p.theta1
			y = np.sin(np.deg2rad(ang))
			x = np.cos(np.deg2rad(ang))
			horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
			connectionstyle = "angle,angleA=0,angleB={}".format(ang)
			kw["arrowprops"].update({"connectionstyle": connectionstyle})
			plt.annotate(env.LABEL_MAP.get(i+1), xy=(x, y), xytext=(1.3*np.sign(x), 1.4*y),horizontalalignment=horizontalalignment, **kw)
		ax.legend(wedges, list(env.LABEL_MAP.values()),title="Species",loc="center right", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
		plt.title("Specie distribution of " + pie_mode[_mode] + " process", fontweight='bold', fontsize=18)
		plt.show()

if __name__ == "__main__":
	barChartVisualizing()
	pieChartVisualizing()