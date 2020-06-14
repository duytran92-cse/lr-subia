import os
import sys
import glob
import shutil
import env
import time

def remove_unmatched_extension(_path, valid_extension):
	for fname in os.listdir(_path):
		if fname.endswith(valid_extension):
			pass
		else:
			os.remove(_path + "/" + fname)
	pass
if __name__ == "__main__":
	start_time = time.time()	
	remove_unmatched_extension(env.BASE_PATH.get('RAW_PATH'), env.BASE_TYPE.get('IMAGE_EXTENSION'))
	remove_unmatched_extension(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations', env.BASE_TYPE.get('LABEL_RAW_EXTENSION'))

	_,imageList = env.getFileList(env.BASE_PATH.get('RAW_PATH') + '/', '*' + env.BASE_TYPE.get('IMAGE_EXTENSION'))
	_,labelList = env.getFileList(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations', '*' + env.BASE_TYPE.get('LABEL_RAW_EXTENSION'))

	archived_images = []
	archived_labels = []

	if len(imageList) < len(labelList):
		for i in range(len(imageList)):
			for j in range(len(labelList)):			
				if(imageList[i].split('.')[0] == labelList[j].split('.')[0]):
					archived_labels.append(labelList[j])
				else:
					pass

	elif len(imageList) > len(labelList):
		for i in range(len(labelList)):
			for j in range(len(imageList)):
				if(labelList[i].split('.')[0] == imageList[j].split('.')[0]):
					archived_images.append(imageList[j])
				else:
					pass
	else:
		for i in range(len(imageList)):
			for j in range(len(labelList)):
				if(imageList[i].split('.')[0] == labelList[j].split('.')[0]):
					pass
				else:
					archived_images.append(imageList[i])
					archived_labels.append(labelList[j])

	for a in range(len(labelList)):
		if len(archived_labels) > 0 and (labelList[a] not in archived_labels):
			shutil.move(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations' + '/' + labelList[a], env.BASE_PATH.get('ORPHAN_PATH') + '/' + 'annotations' + '/' +  labelList[a])

	for b in range(len(imageList)):
		if len(archived_images) > 0 and (imageList[b] not in archived_images):
			shutil.move(env.BASE_PATH.get('RAW_PATH') + '/' + imageList[b], env.BASE_PATH.get('ORPHAN_PATH') + '/' + 'images' + '/' +  imageList[b])
		if len(archived_images) == 0 or len(labelList) == 0 and (imageList[b] in archived_images) or (labelList[b] in archived_labels):
			pass

	end_time = time.time()
	print('--- Finishing after %s seconds ---' % (end_time-start_time))
	print('--- Dataset is synchronized ---')
