# scripts generator, generate scripts in batches

# patrol to inner point, do 1 general attack and then anything

# Load -> patrol to outer point -> do 1 general attack and then anything



import configparser as cfp
from fa2py import Script
ini_config = {'strict':False,'interpolation':None,'inline_comment_prefixes':(';',)}

r = cfp.ConfigParser(**ini_config)
r.optionxform = str
r.read('scripts prototype.ini')

for i in range(6):

    # patrol to point P and attack something A
    # dictionary of attack naming scheme
    attack_dict = {'ANY':1,'STR':2,'INF':4,'TNK':5,'FAC':6,'DEF':7,'POW':9}

    c = 0
    for attack_target in attack_dict:
        for inner_wp in range(34,40):
            script_id = f'P{inner_wp}_{attack_target}'
            data = {"0":f"16,{inner_wp}","1":f"0,{attack_dict[attack_target]}"}
            if attack_target != 'ANY':
                data['2'] = '0,1'
                data['3'] = '59,98'
            script_name = f'patrol to {inner_wp}, attack {attack_target}'
            new_script = Script(script_id,data,script_name)
            r.read_dict(new_script.get_dict())
            r.read_dict({'ScriptTypes':{f'ISSS{700+c}':script_id}})

            outer_wp = (inner_wp - 34) * 4 + 12
            script_id = f'M{outer_wp}_P{inner_wp}_{attack_target}'
            data = {"0":f"3,{outer_wp}","1":f"16,{inner_wp}","2":f"0,{attack_dict[attack_target]}"}
            if attack_target != 'ANY':
                data['3'] = '0,1'
                data['4'] = '59,98'
            script_name = f'move to {outer_wp}, patrol to {inner_wp}, attack {attack_target}'
            new_script = Script(script_id,data,script_name)
            r.read_dict(new_script.get_dict())
            r.read_dict({'ScriptTypes':{f'ISSS{800+c}':script_id}})
            c+=1

with open('scripts.ini', 'w') as outfile:
    r.write(outfile, space_around_delimiters=False)