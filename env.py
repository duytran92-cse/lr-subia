import os
import glob

# get current path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# set image path and label path
BASE_PATH = {
	'RAW_PATH':BASE_DIR + '/' + 'rawData',
	'TRAIN_PATH':BASE_DIR + '/' + 'dataTraining' ,
	'TEST_PATH':BASE_DIR + '/' + 'dataTesting',
	'ORPHAN_PATH':BASE_DIR + '/' + 'orphan',
}

# set image and label extension
BASE_TYPE = {
	'IMAGE_EXTENSION':'.jpg',
	'LABEL_RAW_EXTENSION':'.txt',
	'LABEL_EXTENSION':'.xml',
}

# set label map
LABEL_MAP = {
	1: 'ascidie',
	2: 'ascidieBouche',
	3: 'petoncle',
	4: 'moule',
	5: 'huitre',
	6: 'bryozoaireDense',
	7: 'bryozoaire',
}

# set color for chart
# for more color, please find more at: https://matplotlib.org/3.2.1/tutorials/colors/colors.html
# CHART_COLOR_1 = ['green', 'orange','teal','indigo','pink','red','blue']

CHART_COLOR = {
	1: ('ascidie', '#a8df65'),
	2: ('ascidieBouche', '#66b3ff'),
	3: ('petoncle', '#efb960'),
	4: ('moule', '#ee91bc'),
	5: ('huitre', '#6a097d'),
	6: ('bryozoaire', '#c0392b'),
	7: ('bryozoaireDense', '#a27557')
}

# # count how many files in a folder
def getFileList(_path, _extension=None):
	os.chdir(_path)
	if(_extension is not None):
		fileList = glob.glob(_extension)
	else:
		fileList=[]
	return len(fileList),fileList

# # get color list from chart color
def getColorList():
	color_list = list()
	for _colorKey,_colorData in CHART_COLOR.items():
		color_list.append(_colorData[1])
	return color_list

# print('\033[1m' + 'Hello')

# print(type(list(LABEL_MAP.keys())))
