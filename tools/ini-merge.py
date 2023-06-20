# command line tool for merging ini
# accept an list of file name
# all the files will be written to the first argument

import sys,os
import configparser as cfp

def merge_file(out,list):
	base = cfp.ConfigParser(strict=False,interpolation=None,inline_comment_prefixes=(';',))
	base.optionxform = str
	base.read(list[0])
	
	L2 = list[1:]
		
	for fname in L2:
		f = cfp.ConfigParser(strict=False,interpolation=None,inline_comment_prefixes=(';',))
		f.optionxform = str
		f.read(fname)
		merge_config(base,f)	

	with open(out,'w') as out_file:
		base.write(out_file,space_around_delimiters = False)
		

def merge_config(base,other):
	for s in other.sections():
		if not base.has_section(s):
			base.add_section(s)
			
		for key in other[s]:
			base[s][key] = other[s][key]


# no argument: search for merge.txt, as the merge setting file
# has argument: no command, merge everything into the first file
# 				-r <merge settings>: open merge setting file and merge accordingly
#				-w: write every setting file into the first argument, can be used for overwrite
		
if __name__ == '__main__':
	def file_set(filename):
		with open(filename,'r') as input:
			arr = []
			line = input.readline()
			while line:
				arr.append(line.strip())
				line = input.readline()
			merge_file(arr[0],arr)
	
	if len(sys.argv) == 1:
		file_list = os.listdir()
		if 'merge.txt' in file_list:
			print('"merge.txt" found, start merging files')
			file_set('merge.txt')
		else:
			print('"merge.txt" not found, press any key to exit program')
			
	elif sys.argv[1].startswith('-'):
		if sys.argv[1] == '-r':
			file_set(sys.argv[2])
		elif sys.argv[1] == '-w':
			merge_file(sys.argv[2],sys.argv[3:])
	else:
		merge_file(sys.argv[2],sys.argv[2:])
		print('merge complete')

		
