import sys

sys.path.append('.')
sys.path.append('../')


from utils.vis_vae import VisVAE, get_rules, get_specs
from LogToJson import processing

res_all = []
rules = []
rulesfile = 'DataConvert/trainingdata/rules-cfg1.txt'
with open(rulesfile, 'r') as inputs:
    for line in inputs:
        line = line.strip()
        rules.append(line)

rule2index = {}
for i, r in enumerate(rules):
    rule2index[r] = i

def generate_vector(json, rule2index):
    rules = []
    get_rules(json, 'root', rules)
    behaviors = ['x_position', 'y_position','number',
                 'x_position1','y_position1','x_position2','y_position2',
                 'delta_x','delta_y','scale']

    res_all_part = []
    indices = []
    for j in range(len(rules)):
        add = 'False'
        r = rules[j]
        for b in behaviors:
            if (r.startswith(b))&(add=='False'):
                res = round(float(r.split("->")[1][2:-1]))
                add = 'True'
                indices.append(res)
        if (add=='False'):
            indices.append(rule2index[r])
    return indices

def Log_To_Vector(log):
    return generate_vector(processing([log]), rule2index)

if __name__ == '__main__':

    json = {'type': 'Brush', 'Object_View': 'Map', 'Behavior': {'x_position1': 232, 'x_position2': 300, 'y_position1': 53,'y_position2': 200}}
    res = generate_vector(json, rule2index)
