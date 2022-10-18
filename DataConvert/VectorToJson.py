import re
def transform(rulesfile,vector):
    rules = {}
    with open(rulesfile, 'r') as inputs:
        for line in inputs:
            line = line.strip()
            res = line.split(":")
            rules[int(res[1])] = res[0]
    Type = re.sub(r'\W+', '',rules[vector[-1]].split("->")[1])
    Object_View = re.sub(r'\W+', '',rules[vector[-2]].split("->")[1])
    Behaviors = rules[vector[1]].split("->")[1].split("+")
    Behavior_res = {}
    count = 0
    for value in vector[2:-2]:
        Behavior = re.sub(r'\W+', '',Behaviors[count])
        Behavior_res[Behavior] = value
        print(Behavior,value)
        count = count+1
    res = {}
    res['type'] = Type
    res['Object_View'] = Object_View
    res['Behavior'] = Behavior_res
    return res


if __name__ == '__main__':
    vector = [18, 32,  98.64368 , 92.05296 , 11.968742, 17.83751 ,
       22, 12]
    res = transform('trainingdata/res.txt',vector)
    print(res)