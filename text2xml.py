from xml.etree.ElementTree import Element, SubElement, Comment
import xml.etree.cElementTree as ET
from xml.dom import minidom

import os
from PIL import Image
import glob
import env as env

from xml.dom import minidom
from tqdm import tqdm
import time

def lines_to_list(filename):
	list = []
	with open(filename,"r") as f:
		list = [line.rstrip() for line in f]
	return list

def xml_parsing(file,mode):
	content = lines_to_list(file)

	root = Element('annotation')

	folder = SubElement(root, 'folder')

	if mode == 'train':
		folder.text = env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'train'
	else:
		folder.text = env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'eval'

	filename = SubElement(root, 'filename')
	filename.text = file.split('.')[0] + env.BASE_TYPE.get('IMAGE_EXTENSION')

	path = SubElement(root, 'path')
	if mode == 'train':
		path.text = env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'train' + '/' + file.split('.')[0] + env.BASE_TYPE.get('IMAGE_EXTENSION')
	else:
		path.text = env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'eval' + '/' + file.split('.')[0] + env.BASE_TYPE.get('IMAGE_EXTENSION')

	source = SubElement(root, 'source')
	source_database = SubElement(source, 'database')
	source_database.text = 'Unknown'

	size = SubElement(root, 'size')

	if mode == 'train':
		img = Image.open(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'train' + '/' + file.split('.')[0] + env.BASE_TYPE.get('IMAGE_EXTENSION'))
	else:
		img = Image.open(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'eval' + '/' + file.split('.')[0] + env.BASE_TYPE.get('IMAGE_EXTENSION'))

	width,heigth = img.size
	depth = depth = len(img.getbands())

	size_width = SubElement(size, 'width')
	size_width.text = str(width)
	size_heigth = SubElement(size, 'heigth')
	size_heigth.text = str(heigth)
	size_depth = SubElement(size, 'depth')
	size_depth.text = str(depth)
	segmented = SubElement(root, 'segmented')
	segmented.text = '0'

	for i in range(len(content)):
		object = SubElement(root, 'object')
		object_name = SubElement(object, 'name')

		# mapping labels and name
		for k,v in env.LABEL_MAP.items():
			if content[i].split()[0] == str(k):
				object_name.text = v
			else:
				pass

		object_pose = SubElement(object, 'pose')
		object_pose.text = 'Unspecified'
		object_truncated = SubElement(object, 'truncated')
		object_truncated.text = '0'
		object_difficult = SubElement(object, 'difficult')
		object_difficult.text = '0'
		object_bndbox = SubElement(object, 'bndbox')
		bndbox_xmin = SubElement(object_bndbox, 'xmin')
		bndbox_xmin.text = (content[i].split())[1]
		bndbox_ymin = SubElement(object_bndbox, 'ymin')
		bndbox_ymin.text = (content[i].split())[2]
		bndbox_xmax = SubElement(object_bndbox, 'xmax')
		bndbox_xmax.text = (content[i].split())[3]
		bndbox_ymax = SubElement(object_bndbox, 'ymax')
		bndbox_ymax.text = (content[i].split())[4]

	xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ", encoding='UTF-8')
	with open((file.split('.'))[0] + env.BASE_TYPE.get('LABEL_EXTENSION'), "w") as f:
		f.write(str(xmlstr.decode('UTF-8')))
		f.close()

if __name__ == "__main__":
	start_time = time.time()
	_,fileListTrain = env.getFileList(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + 'train','*' + env.BASE_TYPE.get('LABEL_RAW_EXTENSION'))

	pBarTrain = tqdm(range(len(fileListTrain)))

	for i in pBarTrain:
		pBarTrain.set_description('--- Train data ---')
		time.sleep(0.01)
		xml_parsing(fileListTrain[i],'train')

	_,fileListTest = env.getFileList(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + 'eval','*' + env.BASE_TYPE.get('LABEL_RAW_EXTENSION'))
	
	pBarTest = tqdm(range(len(fileListTest)))
	for k in pBarTest:
		pBarTest.set_description('--- Eval data ---')
		time.sleep(0.01)
		xml_parsing(fileListTest[k],'eval')
	
	end_time = time.time()
	print(' --- Finishing after %s' %(end_time-start_time))
	print('---XML converting is DONE---')
