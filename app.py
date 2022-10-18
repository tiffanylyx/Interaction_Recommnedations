from flask import Flask,request
from flask import jsonify
from flask_cors import CORS
from DataConvert.VectorToJson import transform
from DataConvert.JsonToVector import Log_To_Vector
from Predictor.Predictor import predict
import numpy
from keras.models import load_model
from Predictor.util import result_cleaner


rulesfile = 'DataConvert/trainingdata/res.txt'
rules = {}
rules_count = {'Behavior': [], 'Object_View': [], "type": []}
with open(rulesfile, 'r') as inputs:
    for line in inputs:
        line = line.strip()
        res = line.split(":")
        rules[int(res[1])] = res[0]
        if res[0].startswith('Behavior'):
            rules_count['Behavior'].append(int(res[1]))
        elif res[0].startswith('Object_View'):
            rules_count['Object_View'].append(int(res[1]))
        elif res[0].startswith('type'):
            rules_count['type'].append(int(res[1]))
batch_size = 1
model1 = load_model('Predictor/model/TrainAll_LSTM_V2.h5')
model2 = load_model('Predictor/model/TrainAll_LSTM_V4.h5')
model3 = load_model('Predictor/model/TrainAll_LSTM_V5.h5')
value_range = numpy.load('Predictor/value_range.npy', allow_pickle = True)
value_range = value_range[()]
print(value_range)
#model_list = [model1]
model_list = [model1,model2,model3]
app = Flask(__name__)
cors = CORS(app, resources={r"/getPredict": {"origins": "*"},
	r"/postInteraction": {"origins": "*"},r"/postVisual": {"origins": "*"}})
#CORS(app, supports_credentials=Tru,self.postMsg({'name':self.GLOBAL.Log_file})e)


@app.route('/')
def hello_world():
    return 'Hello World!'

'''
@app.route('/getPredict', methods=['GET'])

def getPredict():
    
    vector = [31, 7, 14, 20, 21, 21, 14.0]
    res = transform(rulesfile,vector)
    response = {
        'msg': res
    }
    print(res)
    return jsonify(response)
'''
@app.route('/postInteraction', methods=['POST'])
def postInteraction():
    anchor = request.json
    print(anchor.get('name')['name'][-1])
    res = []
    if (anchor.get('name')['name'][-1]!=None):
        vector = Log_To_Vector(anchor.get('name')['name'][-1])
        res_vector_all = []
        res_vector_all = predict(vector, model_list,rules,rules_count,value_range)
        for res_vector in res_vector_all:
            if len(res_vector)>1:
                res.append(transform(rulesfile,res_vector))
            else:
                res.append([])
        #res = res.tolist()
        response = {
        'msg': res}
        print('res',response)
        return jsonify(response)

    else:
        return 'response'

@app.route('/postVisual', methods=['POST'])
def postVisual():
    anchor = request.json
    #print('Visual',anchor.get('name'))
    return 'response'

# 启动运行
if __name__ == '__main__':
    app.run()   # 这样子会直接运行在本地服务器，也即是 localhost:5000
   # app.run(host='your_ip_address') # 这里可通过 host 指定在公网IP上运行
