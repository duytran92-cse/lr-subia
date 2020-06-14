import os
import shutil
import env as env
import glob
import sys
import os.path
from os import path
import time
from tqdm import tqdm

def data_partition(train_eval_images):
	_,imagesList = env.getFileList(env.BASE_PATH.get('RAW_PATH'),'*' + env.BASE_TYPE.get('IMAGE_EXTENSION'))
	_,labelsList = env.getFileList(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations','*' + env.BASE_TYPE.get('LABEL_RAW_EXTENSION'))

	name_list = []

	# adding pbar for:
	# 1 : image copy from raw --> 'train' and 'test'

	pbarTrainImg = tqdm(range(train_eval_images))		# get the length of progress bar

	for i in pbarTrainImg:
		pbarTrainImg.set_description('--- Generate dataset ---')
		time.sleep(0.05)
		shutil.copy(env.BASE_PATH.get('RAW_PATH') + '/' + imagesList[i], env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + imagesList[i])
		name_list.append(imagesList[i].split('.')[0])

	for j in range(train_eval_images,len(imagesList),1):
		shutil.copy(env.BASE_PATH.get('RAW_PATH') + '/' + imagesList[j], env.BASE_PATH.get('TEST_PATH') + '/' + 'images' + '/' + imagesList[j])

	for k in range(len(labelsList)):
		if len(name_list) > 0 and labelsList[k].split('.')[0] not in name_list:
			shutil.move(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + labelsList[k], env.BASE_PATH.get('TEST_PATH') + '/' + 'annotations' + '/' + labelsList[k])

def check_subfolders(_path):
	os.chdir(_path)
	if path.isdir('train') and path.isdir('eval'):
		return {'return': 'successful'}
	elif path.isdir('train') and not path.isdir('eval'):
		os.system('mkdir eval')
		return {'return': 'eval missing'}
	elif not path.isdir('train') and path.isdir('eval'):
		os.system('mkdir train')
		return {'return': 'train missing'}
	else:
		os.system('mkdir train eval')
		return {'return': 'missing all'}

def model_partition(train_ratio):	
	lenImageList,imagesList = env.getFileList(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images', '*' + env.BASE_TYPE.get('IMAGE_EXTENSION'))
	lenLabelList,labelsList = env.getFileList(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations', '*' + env.BASE_TYPE.get('LABEL_RAW_EXTENSION'))

	training_amount = abs(round(lenImageList*train_ratio))
	name_list = []

	# defining pbar for each train images and train labels
	pBarTrain = tqdm(range(training_amount))

	#### data partition for training and evaluating (image -- label must match)
	for img_train in pBarTrain:
		pBarTrain.set_description('--- Generate training data ---')
		
		shutil.move(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + imagesList[img_train], env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'train' + '/' + imagesList[img_train])
		name_list.append(imagesList[img_train].split('.')[0])
		time.sleep(0.1)

	for lb_train in range(lenLabelList):	
		if labelsList[lb_train].split('.')[0] in name_list:
			shutil.move(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + labelsList[lb_train], env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + 'train' + '/' + labelsList[lb_train])

	# push the rest to test folder

	for img_test in range(lenImageList):	
		if len(name_list) > 0 and imagesList[img_test].split('.')[0] not in name_list:
			shutil.move(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + imagesList[img_test], env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images' + '/' + 'eval' + '/' + imagesList[img_test])

	for lb_test in range(lenLabelList):	
		if len(name_list) > 0 and labelsList[lb_test].split('.')[0] not in name_list:
			shutil.move(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + labelsList[lb_test], env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + 'eval' + '/' + labelsList[lb_test])

if __name__=='__main__':
	start_time = time.time()
	### section 1
	option = input('Choose mode :')
	if option == 'image' or option == 'IMAGE':
		check_subfolders(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images')
	elif option == 'annotation' or option == 'ANNOTATION':
		check_subfolders(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations')
	elif option == 'all' or option == 'ALL':
		check_subfolders(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'images')
		check_subfolders(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations')
	while(option not in ['image', 'IMAGE', 'annotation', 'ANNOTATION', 'all', 'ALL']):
		print('Syntax Error -- you must select "image" / "IMAGE" or "annotation" / "ANNOTATION" or "all" / "ALL"')
		option = input('Retry another option :')

	print("We have " + str(len(os.listdir(env.BASE_PATH.get('RAW_PATH')))) + " images. Please choose a number < " + str(len(os.listdir(env.BASE_PATH.get('RAW_PATH')))))
	
	### section 2
	number = input("How many images for training model :")
	while int(number)> len(os.listdir(env.BASE_PATH.get('RAW_PATH'))):
		print('Incorrect number')
		number = input("---- Retry ---- :")
	else:
		data_partition(int(number))

	### section 3
	rate = input("Your training rate :")
	while float(rate) <= 0 or float(rate) > 1:
		print('Rate must be in 0 and 1')
		rate = input("---- Retry ---- :")
	else:
		model_partition(float(rate))
	
	end_time = time.time()	
	print('--- Finishing after %s seconds ---' % (end_time-start_time))
	print('--- Dataset is READY---')
