import os
import env as env
import time
import shutil
import glob

def clean_dataset():
	# remove hidden files and directories in image folder
	os.chdir(env.BASE_PATH.get('RAW_PATH'))
	os.system('rm -rf .*')
	[shutil.rmtree(_imageDir) for _file in glob.glob(env.BASE_PATH.get('RAW_PATH') + '/' + '*' + '/')]	

	# remove hidden files and directories in annotation folder
	os.chdir(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations/')
	os.system('rm -rf .*')
	[shutil.rmtree(_labelDir) for _labelDir in glob.glob(env.BASE_PATH.get('TRAIN_PATH') + '/' + 'annotations/' + '/' + '*' + '/')]

if __name__=='__main__':
	start_time = time.time()
	clean_dataset()
	end_time = time.time()
	print('--- Finishing after %s seconds ---' % (end_time-start_time))
	print('--- Dataset is clean ---')
