def processing(line):
    dict_all2 = []

    if len((line))>1:

        for act in line[1:]:
            if (act == [])|('Button-Poet-Value'in act):
                continue
            if ('hover-wordle-select_color-position'in act):
                act = act.split(",")
                dict_res = {}
                dict_res['timestamp'] = act[2]
                dict_res['type'] = 'filter-map-color'
                dict_res['obj'] = act[-2]
                dict_all2.append(dict_res)
                continue
            dict_res = {}
            act = act.split(",")
            dict_res['timestamp'] = act[2]
            dict_res['type'] = act[3]
            dict_res['obj'] = act[4:-1]
            dict_all2.append(dict_res)
        act_all = []

        time_old = float(dict_all2[0]['timestamp'])
        act_old = dict_all2[0]['type']
        for i in dict_all2[1:]:
            time_new = float(i['timestamp'])
            act_new = i['type']
            if not(((time_new-time_old)<0.5)&(act_new == act_old)):
                act_all.append(i)
            time_old = time_new
            act_old = act_new
        dict_all = []
        for i in act_all:
            dict_1 = {}
            dict_2 = {}
            act_type = i['type']
            value = i['obj']
            act = act_type.split("-")

            if act == ['click_hist_index']:
                act = act[0].split("_")
            type1 = act[0].capitalize()
            Object_View = 'None'
            if type1=='Newcereal':
                continue
            Object_View = act[1].capitalize()

            dict_1['Object_View'] = Object_View
            if type1 !='Zoom':
                if (type1=='Hover')|(type1=='Click'):
                    type1='Click'
                    if len(value)>1:
                        behavior = ['x_position','y_position']
                    else:behavior = ['number']
                    for j in range(len(behavior)):
                        b = behavior[j]
                        dict_2[b] = round(float(value[j]))
                elif type1=='Brush':
                    behavior = ['x_position1','y_position1','x_position2','y_position2']
                    for j in range(len(behavior)):
                        b = behavior[j]
                        dict_2[b] = round(float(value[j]))
                elif type1=='Filter':
                    behavior = ['color']
                    print('value',value)
                    for j in range(len(behavior)):
                        b = behavior[j]
                        dict_2[b] = round(float(value[j]))
                '''
                elif type1=='Newcereal':
                    behavior = ['value']
                    for j in range(len(behavior)):
                        b = behavior[j]
                        dict_2[b] = value[j]
                '''
            else:
                behavior = ['delta x','delta y','scale']
                dict_2['delta_x'] = round(float(value[0][10:]))
                dict_2['delta_y'] = round(float(value[1].split('scale')[0][:-2]))
                dict_2['scale'] = round(float(value[1].split('scale')[1][1:-1]),2)


            dict_1['type'] = type1
            dict_1['Behavior'] = dict_2
            dict_all.append(dict_1)
        return dict_all
    else:
        dict_1 = {}
        dict_2 = {}
        act = line[0]
        dict_res = {}
        dict_res['timestamp'] = act[1]
        dict_res['type'] = act[2]
        dict_res['obj'] = act[3:-1]
        act_type = dict_res['type']
        value = dict_res['obj']
        act = act_type.split("-")
        if act == ['click_hist_index']:
            act = act[0].split("_")
        type1 = act[0].capitalize()
        Object_View = 'None'
        if type1 != 'Newcereal':
            Object_View = act[1].capitalize()

        dict_1['Object_View'] = Object_View
        if type1 != 'Zoom':
            if (type1 == 'Hover') | (type1 == 'Click'):
                type1 = 'Click'
                if len(value) > 1:
                    behavior = ['x_position', 'y_position']
                else:
                    behavior = ['number']
                for j in range(len(behavior)):
                    b = behavior[j]
                    dict_2[b] = round(float(value[0][j]))
            elif type1 == 'Brush':
                behavior = ['x_position1', 'y_position1', 'x_position2', 'y_position2']
                dict_2['x_position1'] = round(float(value[0][0]))
                dict_2['y_position1'] = round(float(value[0][1]))
                dict_2['x_position2'] = round(float(value[1][0]))
                dict_2['y_position2'] = round(float(value[1][1]))
            '''
            elif type1 == 'Newcereal':
                behavior = ['value']
                for j in range(len(behavior)):
                    b = behavior[j]
                    dict_2[b] = value[j]
            '''

        else:
            behavior = ['delta x', 'delta y', 'scale']
            dict_2['delta_x'] = round(float(value[0][10:]))
            dict_2['delta_y'] = round(float(value[1].split('scale')[0][:-2]))
            dict_2['scale'] = round(float(value[1].split('scale')[1][1:-1]), 2)

        dict_1['type'] = type1
        dict_1['Behavior'] = dict_2

        return dict_1

if __name__=='__main__':

    import os
    path = 'DataConvert/sourcedata/log_file'
    fileList = os.listdir(path)
    dict_all = []
    for f in os.listdir(path):
        if f=='.DS_Store':
            continue
        f_name = path+'/'+f
        f2 = open(f_name)
        lines = f2.readlines()
        line = []
        for line3 in lines:
            line.append(line3)
        res = processing(line[:-1])
        dict_all.append(res)
    dict_res = {'dict_all':dict_all}


    import json
    json_str = json.dumps(dict_res)
    with open('DataConvert/sourcedata/data_log.json', 'w') as json_file:
        json_file.write(json_str)
    '''
    import os
    import numpy as np
    path = 'interaction_with_visual.npy'
    dict_all = np.load(path, allow_pickle=True)
    res_all = []
    for f in (dict_all):
        #print(f)
        res = processing(f)
        res_all.append(res)
    dict_res = {'dict_all':res_all}


    import json
    json_str = json.dumps(dict_res)
    with open('DataConvert/sourcedata/test_data22.json', 'w') as json_file:
        json_file.write(json_str)
    '''
