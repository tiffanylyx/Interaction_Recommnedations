
import sys
sys.path.append("..")
import simplejson as json

import numpy as np

from DataConvert.utils.vis_vae import VisVAE, get_rules, get_specs


# extract CFG rules from the dataset
def extract_rules(inputfile, outputfile):
    specs = []

    with open(inputfile, 'r') as inputs:
        json_data = json.load(inputs)
        specs = json_data['dict_all']

    allrules = {}

    max_rulelen = 0
    for spec1 in specs:
        for spec in spec1:
            rules = []
            get_rules(spec, 'root', rules)
            for r in rules:
                if not r in allrules:
                    allrules[r] = 0
                allrules[r] += 1
            max_rulelen = max(max_rulelen, len(rules))

    allrules = sorted(allrules.keys())
    allrules.append('Nothing -> None')
    behaviors = ['x_position', 'y_position','number',
                 'x_position1','y_position1','x_position2','y_position2',
                 'delta_x','delta_y','scale']
    allrules2 = []

    for r in allrules:
        res = r
        for behavior in behaviors:
            if r.startswith(behavior):
                res = behavior+' -> '+'None'

        allrules2.append(res)

    allrules2 = list(set(allrules2))
    with open(outputfile, 'w') as outf:
        for r in allrules2:
            outf.write(r + '\n')

# generate the traning and testing datasets
def generate_datasets(inputfile, rulesfile, outputdir):
    res_all = []
    rules = []
    with open(rulesfile, 'r') as inputs:
        for line in inputs:
            line = line.strip()
            rules.append(line)
    print('number of rules: %d' % len(rules))

    rule2index = {}
    for i, r in enumerate(rules):
        rule2index[r] = i
    print('rule2index', rule2index)
    with open(outputdir + '/res.txt', 'w') as outf:
        for r in rule2index:
            outf.write(r + ':' + str(rule2index[r]) + '\n')

    with open(inputfile, 'r') as inputs:
        json_data = json.load(inputs)
        specs = json_data['dict_all']
        for spec1 in specs:
            data = []
            for spec in spec1:
                rules = []
                get_rules(spec, 'root', rules)
                data.append(rules)
            behaviors = ['x_position', 'y_position','number',
                         'x_position1','y_position1','x_position2','y_position2',
                         'delta_x','delta_y','scale']

            res_all_part = []
            for i, sentence_rules in enumerate(data):
                indices = []
                for j in range(len(sentence_rules)):
                    add = 'False'
                    r = sentence_rules[j]
                    for b in behaviors:
                        if (r.startswith(b))&(add=='False'):
                            res = round(float(r.split("->")[1][2:-1]))
                            add = 'True'
                            indices.append(res)
                    if (add=='False'):
                        indices.append(rule2index[r])
                res_all_part.append(indices)
            res_all.append(res_all_part)
            print('res_all_part',res_all_part)
        np.save(outputdir+'/res.npy', res_all,'dtype=object')
