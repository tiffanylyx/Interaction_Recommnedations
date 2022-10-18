import numpy as np

def find_closed(number_list, value):
  min_value = 10000
  closest = 0
  for i in number_list:
    a = abs(i-value)
    if a<min_value:
      closest = i
      min_value = a
  return closest


def result_cleaner(predict,value_range,rules,rules_count):
  predict[-2] = round((find_closed([0,1.49,1.6,3],predict[-2]*(len(rules_count['Object_View'])+1)-1)))
  predict[-1] = round((find_closed([0,1.49,1.6,3],predict[-1]*(len(rules_count['type'])+1)-1)))

  predict[-2] = rules_count['Object_View'][int(predict[-2])]
  predict[-1] = rules_count['type'][int(predict[-1])]
  if predict[-1] == list(rules.keys())[list(rules.values()).index('type -> "Filter"')]:
    predict[0] = find_closed(rules_count['color'],i[0])
  Type = predict[-1]
  Object_View = predict[-2]
  if rules[Type]=='type -> "Brush"':
    Object_View = list(rules.keys())[list(rules.values()).index('Object_View -> "Map"')]
    Behavior = list(rules.keys())[list(rules.values()).index('Behavior -> x_position1 "+" x_position2 "+" y_position1 "+" y_position2')]
    save = predict[:4]
    brush_x1 = value_range['brush_x1']
    brush_width = value_range['brush_width']
    brush_y1 = value_range['brush_y1']
    brush_height = value_range['brush_height']
    save[0] = save[0]*(brush_x1[1]-brush_x1[0])+brush_x1[0]
    save[1] = save[1]*(brush_width[1]-brush_width[0])+brush_width[0]
    save[1] = save[0]+save[1]
    save[2] = save[2]*(brush_y1[1]-brush_y1[0])+brush_y1[0]
    save[3] = save[3]*(brush_height[1]-brush_height[0])+brush_height[0]
    save[3] = save[2]+save[3]
    print('brush',save)
  elif rules[Type]=='type -> "Filter"':
    color = value_range['color']
    Object_View = list(rules.keys())[list(rules.values()).index('Object_View -> "Map"')]
    Behavior = list(rules.keys())[list(rules.values()).index('Behavior -> color')]
    save = [predict[0]]
    save[0] = save[0]*(color[1]-color[0])+color[0]
  elif rules[Type]=='type -> "Zoom"':
    delta_x = value_range['delta_x']
    delta_y = value_range['delta_y']
    scale = value_range['scale']
    Object_View = list(rules.keys())[list(rules.values()).index('Object_View -> "Map"')]
    Behavior = list(rules.keys())[list(rules.values()).index('Behavior -> delta_x "+" delta_y "+" scale')]
    save = predict[:3]
    save[0] = save[0]*(delta_x[1]-delta_x[0])+delta_x[0]
    save[1] = save[1]*(delta_y[1]-delta_y[0])+delta_y[0]
    save[2] = save[2]*(scale[1]-scale[0])+scale[0]

  elif rules[Type]=='type -> "Click"':
    if (rules[Object_View] == 'Object_View -> "Hist"'):
      number = value_range['number']
      Behavior = list(rules.keys())[list(rules.values()).index('Behavior -> number')]
      save = [predict[0]]
      save[0] = save[0]*(number[1]-number[0])+number[0]
    else:
      Behavior = list(rules.keys())[list(rules.values()).index('Behavior -> x_position "+" y_position')]
      x_position = value_range['x_position']
      y_position = value_range['y_position']
      save = predict[:2]
      save[0] = save[0]*(x_position[1]-x_position[0])+x_position[0]
      save[1] = save[1]*(y_position[1]-y_position[0])+y_position[0]

  predict_full = [18,Behavior]
  for value in save:
    predict_full.append(np.float(value))
  predict_full.append(Object_View)
  predict_full.append(Type)
  return predict_full

def padding_data(vector, max_len = 8):
    compute_mean = [0.22727376808939367, 0.36979989130109175, 0.3701369591107582]
    if len(vector)==5:
        vector[3:3] = compute_mean
    elif len(vector)==6:
        vector[4:4] = compute_mean[1:]
    elif len(vector)==7:
        vector[5:5] = compute_mean[2:]
    return np.array(vector[2:])

def input_cleaner(i, value_range,rules,rules_count):
    if len(i)==8:
      print(value_range,value_range['brush_x1'])
      i[3] = i[3]-i[2]
      i[5] = i[5]-i[4]
      i[2] = (i[2]-value_range['brush_x1'][0])/(value_range['brush_x1'][1]-value_range['brush_x1'][0])
      i[3] = (i[3]-value_range['brush_width'][0])/(value_range['brush_width'][1]-value_range['brush_width'][0])
      i[4] = (i[4]-value_range['brush_y1'][0])/(value_range['brush_y1'][1]-value_range['brush_y1'][0])
      i[5] = (i[5]-value_range['brush_height'][0])/(value_range['brush_height'][1]-value_range['brush_height'][0])
    elif i[1]== list(rules.keys())[list(rules.values()).index('Behavior -> color')]:
      i[2] = (i[2]-value_range['color'][0])/(value_range['color'][1]-value_range['color'][0])
    elif i[1]== list(rules.keys())[list(rules.values()).index('Behavior -> delta_x "+" delta_y "+" scale')]:
      delta_x = value_range['delta_x']
      delta_y = value_range['delta_y']
      scale = value_range['scale']
      i[2] = (i[2]-delta_x[0])/(delta_x[1]-delta_x[0])
      i[3] = (i[3]-delta_y[0])/(delta_y[1]-delta_y[0])
      i[4] = (i[4]-scale[0])/(scale[1]-scale[0])

    elif i[1]== list(rules.keys())[list(rules.values()).index('Behavior -> number')]:
      number = value_range['number']
      i[2] = (i[2]-number[0])/(number[1]-number[0])
    elif i[1]== list(rules.keys())[list(rules.values()).index('Behavior -> x_position "+" y_position')]:
      x_position = value_range['x_position']
      y_position = value_range['y_position']
      i[2] = (i[2]-x_position[0])/(x_position[1]-x_position[0])
      i[3] = (i[3]-y_position[0])/(y_position[1]-y_position[0])
    i[-1] = (rules_count['type'].index(i[-1])+1)/(len(rules_count['type'])+1)
    i[-2] = (rules_count['Object_View'].index(i[-2])+1)/(len(rules_count['Object_View'])+1)
    return i