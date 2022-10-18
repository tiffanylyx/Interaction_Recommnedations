/* eslint-disable */
import Vue from 'vue'
import App from './App.vue'
import global_ from './components/Global'//引用文件
import axios from 'axios'
import VueAxios from 'vue-axios'
import Bus from './assets/bus.js';
Vue.prototype.GLOBAL = global_//挂载到Vue实例上面
Vue.config.productionTip = false

new Vue({
    data: function(){
        return {
            age_select: []
        }
    },
  render: h => h(App)
}).$mount('#app')

axios.defaults.baseURL = 'http://127.0.0.1:5000';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
Vue.use(VueAxios, axios)
/*
Vue.prototype.getPredict = function (a){
  const path = 'http://localhost:5000/getPredict';
  const axios = require('axios');

var fianl_res = makeGetRequest();
async function makeGetRequest() {

  let res = await axios.get('http://localhost:5000/getPredict');

  result = res.data;
  console.log('res2',result );
  return result
}
console.log('res1',fianl_res)
}

*/
Vue.prototype.getPredict = function (){
  const path = 'http://localhost:5000/getPredict';
  const axios = require('axios');
async function makeGetRequest() {

  let res = await axios.get('http://localhost:5000/getPredict');
  var result = res.data['msg'];

  Bus.$emit("Get_Predict", result)
  return result
}
var fianl_res = makeGetRequest();
console.log('fianl_res',fianl_res)
return fianl_res
}

Vue.prototype.postInteraction = function (data){
  const path1 = 'http://localhost:5000/postInteraction';
  axios.post(path1,{name: data}).then((res)=>(Bus.$emit("Get_Predict", res.data.msg),console.log('this.msg',res.data.msg)))
}

Vue.prototype.postVisual = function (data){
  const path2 = 'http://localhost:5000/postVisual';
  axios.post(path2,{name: data})
}