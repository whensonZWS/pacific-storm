import os
import configparser as cfp
import yaml
from fa2py import Team

basepath = os.path.split(os.path.abspath(__file__))[0]

# triggers
ini_config = {'strict':False,'interpolation':None,'inline_comment_prefixes':(';',)}

uid_counter = 0
def uid():
    global uid_counter
    result = f'ISS_TEAM_{uid_counter:03}'
    uid_counter += 1
    return result

# def ignore_case_in(item,d):
#     return item.lower() in [key.lower() for key in d]

# def ignore_case_set(d, key, value):
#     for original_key in d:
#         if key.lower() == original_key.lower():
#             d[original_key] = value
#             return



def case_helper(key,d):
    for original_key in d:
        if key.lower() == original_key.lower():
            return str(original_key)
    return ''

with open(os.path.join(basepath,'teams.yaml'),'r') as input_file:
    yaml_file = yaml.safe_load(input_file)

out = cfp.ConfigParser(**ini_config)
out.optionxform = str

team_types_sn = dict()
team_types_sn['TeamTypes'] = dict()


teams = yaml_file['Teams']
for item in teams:
    team_id = item[case_helper('team_id',item)]
    taskforce = item[case_helper('taskforce',item)]
    script = item[case_helper('script',item)]

    t = Team(team_id,taskforce,script)
    custom_options = ['Max','Full','Name','Group','House','Whiner','Droppod','Suicide','Loadable','Prebuild','Priority','Waypoint','Annoyance','IonImmune','Recruiter','Reinforce','TechLevel','Aggressive','Autocreate','GuardSlower','OnTransOnly','AvoidThreats','LooseRecruit','VeteranLevel','IsBaseDefense','UseTransportOrigin','MindControlDecision','OnlyTargetHouseEnemy','TransportsReturnOnUnload','AreTeamMembersRecruitable']
    team_types_sn['TeamTypes'][uid()] = item['team_id']

    for opt in custom_options:
        if case_helper(opt,item):
            t.set({opt:item[case_helper(opt,item)]})

    out.read_dict(t.get_dict())


out.read_dict(team_types_sn)



with open(os.path.join(basepath,'teams.ini'), 'w') as sample_file:
    out.write(sample_file, space_around_delimiters=False)

