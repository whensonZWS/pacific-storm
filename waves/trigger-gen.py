import os
import configparser as cfp
import yaml
from fa2py import Trigger, Action, Event

basepath = os.path.split(os.path.abspath(__file__))[0]

# triggers
ini_config = {'strict':False,'interpolation':None,'inline_comment_prefixes':(';',)}

uid_counter = 0
def uid():
    global uid_counter
    result = (f'ISS_TAG_UID_{uid_counter:03}',f'ISS_TRG_UID_{uid_counter:03}')
    uid_counter += 1
    return result

with open(os.path.join(basepath,'triggers.yaml'),'r') as input_file:
    yaml_file = yaml.safe_load(input_file)

out = cfp.ConfigParser(**ini_config)
out.optionxform = str


triggers = yaml_file['Triggers']

# processing trigger/tag id/name
for item in triggers:
    if 'trigger_id' in item:
        trigger_id = item['trigger_id']
        if 'tag_id' in item:
            tag_id = item['tag_id']
        else:
            if trigger_id.startswith('ISS_TRG'):
                tag_id = trigger_id.replace('TRG','TAG')
            else:
                tag_id = uid()[0]

    else:
        tag_id, trigger_id = uid()


    if 'trigger_name' in item:
        trigger_name = item['trigger_name']
        if 'tag_name' in item:
            tag_name = item['tag_name']
        else:
            tag_name = f'{trigger_name}(tag)'
    else:
        tag_name,trigger_name = ('unnamed tag','unnamed trigger')

    t = Trigger(tag_id,trigger_id,tag_name,trigger_name)
    # processing custom items
    custom_options = ['easy','medium','hard','disabled','type','house']
    for opt in custom_options:
        if opt in item:
            t.__dict__[opt] = item[opt]

    if 'events' in item and item['events']:
        for event in item['events']:
            if 'p' in event:
                if type(event['p']) is list:
                    t.add_events(Event(event['type'],event['p']))
                else:
                    t.add_events(Event(event['type'],[event['p']]))
            else:
                t.add_events(Event(event['type'],list()))

    if 'actions' in item and item['actions']:
        for action in item['actions']:
            if 'p' in action:
                if type(action['p']) is list:
                    t.add_actions(Action(action['type'],action['p']))
                else:
                    t.add_actions(Action(action['type'],[action['p']]))
            else:
                t.add_actions(Action(action['type'],list()))
    out.read_dict(t.get_dict())

with open(os.path.join(basepath,'triggers.ini'), 'w') as sample_file:
    out.write(sample_file, space_around_delimiters=False)

