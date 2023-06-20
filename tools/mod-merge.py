
import configparser as cfp
import sys,os
# validate an input string and return boolean
# if the string is valid, return an list 
def demo_validator(s,L):
	if s.startswith(';-demo:'):
		if s.count('[') == 1 and s.count(']') == 1 and s.count('=') == 1:
			L[0] = s[s.find('[')+1 : s.find(']')]
			L[1] = s[s.find(']')+1 : s.find('=')]
			L[2] = s[s.find('=')+1 : ]
			if L[0] and L[1] and L[2]:
				return True
	return False

register_list = {'InfantryTypes','VehicleTypes','AircraftTypes','BuildingTypes',
	'WeaponTypes','Projectiles','Warheads','SuperWeaponTypes',
	'VoxelAnims','Animations','Particles','ParticleSystems',
	'TunnelTypes','OverlayTypes','SmudgeTypes','TerrainTypes'}


def parse_arg(L):
	rules_name = ''
	overwrite = ''
	demo = []
	pos_r = len(L)
	pos_o = len(L)
	pos_d1 = len(L)
	pos_d2 = len(L)
	if '-rules' in L:
		pos_r = L.index('-rules')
		rules_name = L[pos_r + 1]
	
	if '-o' in L:
		pos_o = L.index('-o')
		overwrite = L[pos_o + 1]
	
	if '-demo' in L:
		pos_d1 = L.index('-demo')
		pos_d2 = pos_d1 + 1
		while pos_d2<len(L) and not L[pos_d2].startswith('-'):
			pos_d2 += 1
		demo = L[pos_d1+1:pos_d2]
	#print(rules_name,overwrite,demo)
	argv = [L[s] for s in range(len(L)) if s not in (pos_r,pos_r+1,pos_o,pos_o+1) and s not in range(pos_d1,pos_d2)]
	
	# load base file, and rules file, if it exists
	base = cfp.ConfigParser(strict=False,interpolation=None,inline_comment_prefixes=(';',))
	base.optionxform = str
	if argv:
		base.read(argv[0],encoding='UTF-8')
		print('load: %s' % argv[0])
	
	
	rules = cfp.ConfigParser(strict=False,interpolation=None,inline_comment_prefixes=(';',))
	rules.optionxform = str
	if rules_name:
		rules.read(rules_name,encoding='UTF-8')
		print('load: %s' % rules_name)
	
	# create an index of existing item and indexing, to speed up and save memory
	
	dic = {}
	sn = {}
	
	for r in register_list:
		
		dic[r] = set()
		sn[r] = 0
		
		if base.has_section(r):
			for i in base[r]:
				dic[r].add(base[r][i])
				if int(i) > sn[r]:
					sn[r] = int(i)
		
		if rules.has_section(r):
			for i in rules[r]:
				dic[r].add(rules[r][i])
				if int(i) > sn[r]:
					sn[r] = int(i)
		
		# if index doesn't exist at all:
		
		if sn[r] == 0:
			sn[r] = 10000
					
			
	def merge_module(module_name,demo_mode = False):
		module = cfp.ConfigParser(strict=False,interpolation=None,inline_comment_prefixes=(';',))
		module.optionxform = str
		module.read(module_name,encoding='UTF-8')
		
		if demo_mode:
			with open(module_name,'r',encoding='UTF-8') as in_file:
				line = in_file.readline()
				while line and not line.startswith('['):
					temp = ['','','']
					if demo_validator(line.strip(),temp):
						if not module.has_section(temp[0]):
							module.add_section(temp[0])
						module[temp[0]][temp[1]] = temp[2]
					line = in_file.readline()
			
		for s in module.sections():
			if s in register_list:
				for i in module[s]:
					register(s,module[s][i])
			else:
				if not base.has_section(s):
					base.add_section(s)
				for key in module[s]:
					base[s][key] = module[s][key]
	
	def register(s,id):
		if id not in dic[s]:
			if not base.has_section(s):
				base.add_section(s)
			sn[s] += 1
			base[s][str(sn[s])] = id
			dic[s].add(id)
	
	L2 = argv[1:]
	
	
	for module in L2:
		merge_module(module)
		print('done: %s' % module)
	
	if demo:
		print('------ demo mode ------')
	
	for module in demo:
		merge_module(module,True)
		print('done: %s' % module)
		
	if overwrite == '':
		overwrite = argv[0]
	
	with open(overwrite,'w') as out_file:
		base.write(out_file,space_around_delimiters = False)
		
def file_set(filename):
		with open(filename,'r') as input:
			arr = []
			line = input.readline()
			while line:
				if line.strip() != '':
					arr.append(line.strip())
				line = input.readline()
			parse_arg(arr)
			
if __name__ == '__main__':
			
	if len(sys.argv) == 1:
		file_list = os.listdir()
		if 'module.txt' in file_list:
			print('"module.txt" found')
			file_set('module.txt')
			
	elif sys.argv[1].startswith('-'):
		if sys.argv[1].lower() == '-r':
			file_set(sys.argv[2])
			
	else:
		parse_arg(sys.argv[1:])
		
		
		
				
				
	

		