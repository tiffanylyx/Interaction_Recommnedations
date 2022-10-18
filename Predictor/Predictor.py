import sys
import numpy as np
sys.path.append('../Predictor')

from keras.models import load_model
from util import result_cleaner,padding_data,input_cleaner

# 这个值需要根据实际情况改的

batch_size = 1
vector_all = []
def predict(vector, model_list,rules,rules_count,value_range):
    vector = input_cleaner(vector,value_range,rules,rules_count)
    vector = padding_data(vector)
    print('vector',vector)
    vector_all.append(vector)
    res = []
    if len(vector_all)>3:
        predictX = np.array(vector_all[-3:])
        predictX = predictX.reshape([1,3,6])
        for model in model_list:
            testPredict = model.predict(predictX, batch_size=batch_size)
            print('testPredict',testPredict)
            res.append(result_cleaner(testPredict[0] ,value_range,rules,rules_count))
        return res
    else:
        return []
