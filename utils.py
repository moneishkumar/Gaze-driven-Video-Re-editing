import yaml
import os,sys

def readYaml(filename):

	if not os.path.exists(filename):
		print("File does not exist: %s"%(filename))
		exit()

	file_obj= open(filename,'r')
	data = yaml.load(file_obj)
	return data

if __name__ == '__main__':
	main()