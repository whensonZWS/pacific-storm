import os
import configparser as cfp

basepath = os.path.split(os.path.abspath(__file__))[0]


ini_config = {'strict':False,'interpolation':None,'inline_comment_prefixes':(';',)}

#input trigger description from fadata.ini

fc = cfp.ConfigParser(**ini_config)
fc.optionxform = str
fc.read(os.path.join(basepath,"fadata.ini"))
eventsRA2=[]
actionsRA2=[]

# entry = [description,p1,p2.....]

for key in fc['EventsRA2']:
	temp = fc['EventsRA2'][key].split(',')
	eventsRA2.append([temp[0],int(temp[1]),int(temp[2])])
	
for key in fc['ActionsRA2']:
	temp = fc['ActionsRA2'][key].split(',')
	actionsRA2.append([temp[0],int(temp[1]),int(temp[2]),
		int(temp[3]),int(temp[4]),int(temp[5]),int(temp[6]),int(temp[7])])

# #input script description from yrscript.ini
# sc = cfp.ConfigParser(**ini_config)
# sc.optionxform = str
# sc.read("yrscript.ini")

# #sd: script action description
# sd = {}

# for key in sc['ActionTypes']:
	# arr = sc['ActionTypes'][key].split(',')
	# sd[key] = (arr[0],arr[1])

# Class Delecration for Map Editor
# class trigger 
# Trigger(tag_id, trigger_id, TagName, TriggerName, 
# Settings = [], Events = [], Actions = [])

# attributes:
# nEvents: number of events
# nActions: number of events
# direct access: easy, medium, hard, disabled, linked triggers, type
#		actions, events

# methods:
# add_actions(*Actions)
# add_events(*Events)

# not implemented
# get_ini(): return an configparser object that includes all the ini


class Trigger:

	def __init__(self, tag_id, trigger_id, tag_name='unnamed tag',trigger_name='unnamed trigger'):
		self.tag_id = tag_id
		self.trigger_id = trigger_id
		self.tag_name = tag_name
		self.trigger_name = trigger_name
		self.easy = 1
		self.medium = 1
		self.hard = 1
		self.disabled = 0
		self.link = '<none>'
		self.type = 0
		self.actions = []
		self.events = []
		self.house = 'UnitedStates'
		self.nActions = 0
		self.nEvents = 0
		
	def add_actions(self,*args):
		self.actions.extend(args)
		self.nActions += len(args) 
	
	def add_events(self,*args):
		self.events.extend(args)
		self.nEvents += len(args)
		
	def get_dict(self):
		# return a dictionary r representing all the triggers info
		r = {}
		r ['Tags'] = {}
		r ['Triggers'] = {}
		r ['Actions'] = {}
		r ['Events'] = {}
		
		
		# Tags
		r['Tags'][self.tag_id] = '{},{},{}'.format(self.type,self.tag_name,self.trigger_id)
		
		# Triggers
		r['Triggers'][self.trigger_id] = '{},{},{},{},{},{},{},0'.format(self.house,self.link,
			self.trigger_name,self.disabled,self.hard,self.medium,self.easy)
		
		# Actions
		temp = str(self.nActions)
		for i in range(self.nActions):
			temp += ',' + str(self.actions[i])
		r['Actions'][self.trigger_id] = temp
		
		# Events
		temp = str(self.nEvents)
		for i in range(self.nEvents):
			temp += ',' + str(self.events[i])
		r['Events'][self.trigger_id] = temp
		
		return r
	


class Action:
	def __init__(self, type=0, p=list()):
		self.type = type
		self.parameter(p)
		
	def parameter(self, p):
		self.p = ['0'] * 7
		pos = 0
		L = actionsRA2[self.type]
		for i in range(1,6):
			if L[i] < 0:
				self.p[i-1] = str(-L[i])
			elif L[i] > 0:
				self.p[i-1] = str(p[pos])
				pos += 1	
		
		if L[7] == 1:
			self.p[6] = str(wp(p[pos]))
		else:
			self.p[6] = 'A'
			
	
	def __str__(self):
		r = str(self.type)
		for item in self.p:
			r += ',' + item
		return r
			

class Event:
	def __init__(self, type=0, p=list()):
		self.type = type
		self.parameter(p)
	
	def parameter(self, p):
		L = eventsRA2[self.type]
		if L[1] != 0:
			self.p = ['0'] * 3
			self.p[0] = '2'
			self.p[1] = str(p[0])
			self.p[2] = str(p[1])
			
		else:
			self.p = ['0'] * 2
			if L[2] != 0:
				self.p[1] = str(p[0])
		
	def __str__(self):
		r = str(self.type)
		for item in self.p:
			r += ',' + item
		return r

class TaskForce:
	def __init__(self, taskforce_id, name='unnamed taskforce', data={}, group=-1):
		self.units = dict(data)
		self.taskforce_id = taskforce_id
		self.name = name
		self.group = group
		
	def set_units(self,number,unit):
		self.units[unit] = number
		
	def get_dict(self):
		d = {}
		d[self.taskforce_id] = {}
		index = 0
		for unit in self.units:
			d[self.taskforce_id][str(index)] = str(self.units[unit]) + ',' + unit
			index += 1
		d[self.taskforce_id]['Name'] = self.name
		d[self.taskforce_id]['Group'] = str(self.group)
		
		return d
		
class Script:
	# internal data is stored in dictionary
	def __init__(self, script_id, data, name='unnamed script', options=dict()):
		self.data = dict(data)
		self.script_id = script_id
		self.set({'Name':name})
		self.set(options)
		
		
	def set(self,options):
		for key in options:
			self.data[key] = options[key]
	
	def get_dict(self):
		d = dict()
		d[self.script_id] = dict(self.data)
		#d['ScriptTypes'] = {'000231':self.script_id}

		return d
	
		
class Team:

	def __init__(self, team_id, taskforce, script, name='unnammed team', options={}):
		self.data = dict()
		self.team_id = team_id
		self.set({
			'Max': '5',
			'Full': 'no',
			'Name': name,
			'Group': '-1',
			'House': '<none>',
			'Script': script,
			'Whiner': 'no',
			'Droppod': 'no',
			'Suicide': 'no',
			'Loadable': 'yes',
			'Prebuild': 'no',
			'Priority': '5',
			'Waypoint': 'A',
			'Annoyance': 'no',
			'IonImmune': 'no',
			'Recruiter': 'no',
			'Reinforce': 'no',
			'TaskForce': taskforce,
			'TechLevel': '0',
			'Aggressive': 'yes',
			'Autocreate': 'no',
			'GuardSlower': 'no',
			'OnTransOnly': 'no',
			'AvoidThreats': 'no',
			'LooseRecruit': 'no',
			'VeteranLevel': '1',
			'IsBaseDefense': 'no',
			'UseTransportOrigin': 'no',
			'MindControlDecision': '0',
			'OnlyTargetHouseEnemy': 'no',
			'TransportsReturnOnUnload': 'no',
			'AreTeamMembersRecruitable': 'no',
		})
		
		
		
	def set(self,options):
		for key in options:
			self.data[key] = str(options[key])
			if options[key] is True:
				self.data[key] = 'yes'
			elif options[key] is False:
				self.data[key] = 'no'
				
			
	def get_dict(self):
		d = {}
		d[self.team_id] = dict(self.data)
		return d
	

# helper method
# convert waypoint from number into alphabet format
# conversion is like excel column index
# 0-> A, 25 -> Z, 26 -> AA, 52 -> BA

def wp(i):
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	i = int(i)
	first = i // 26-1
	second = i % 26
	result = ""
	if first >= 0:
		result = result + alphabet[first]
	result = result + alphabet[second]
	return result
	
if __name__ == '__main__':
	
	t = Trigger('ISS_TAG000','ISS_TRI000')
	t.add_actions(Action(11,['NOSTR:This is sample text']))
	t.add_events(Event(13,[10]))
	
	s = t.get_dict()
	r = cfp.ConfigParser(**ini_config)
	r.optionxform = str
	
	r.read('fa sample triggers.ini')
	r.read_dict(s)
	
	with open('fa sample triggers.ini', 'w') as sample_file:
		r.write(sample_file, space_around_delimiters=False)