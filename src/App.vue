/* eslint-disable */
<template>
  <div id="main" style="width:1204px">
    <div id="Button" style="border-top: 2px solid #AAA;border-left: 2px solid #AAA;border-right: 2px solid #AAA;border-bottom: 2px dashed #AAA">
      <Button/>
    </div>
    <div id="UI" style="width:1240px;height:700px">
    <div id="Selecter" style="width:300px;height:100px;float:left;border-left: 2px solid #AAA">
      <Selecter/>
    </div>

    <div id="poem" style="width:300px;height:599px;float:left;border-left: 2px solid #AAA;border-top: 2px dashed #AAA;border-bottom: 2px solid #AAA;">
      <div id = 'Wordle'>
        <Wordle/>
      </div>
    </div>
    <div id="map" style="width:500px;height:701px;float:left;border-bottom: 2px solid #AAA;border-left: 2px dashed #AAA">
      <Map msg="Welcome to Your Vue.js App"/>
    </div>
    <div id='charts' style="float:left;border-left: 2px dashed #AAA;border-right: 2px solid #AAA;border-bottom: 2px solid #AAA">
      <div id='forceplot' style="width:400px;height:339px;">
        <Force/>
      </div>
      <div id='histplot' style="width:400px;height:339px;float:left;border-top: 2px dashed #AAA">
        <Hist msg="Welcome to Your Vue.js App"/>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import Selecter from './components/Selecter.vue'
import Map from './components/Map.vue'
import Hist from './components/Hist.vue'
import Force from './components/Force.vue'
import Wordle from './components/Wordle.vue'
import Button from './components/Button.vue'


export default {
  name: 'App',
  components: {
    Button,
    Selecter,
    Map,
    Hist,
    Force,
    Wordle
  }}



</script>

<style>
#UI{position:relative} 
#Selecter{ position:absolute;left:0px;top:0px;z-index:0} 
/* div背景色为红色 */ 
#poem{ position:absolute;left:0px;top:100px;z-index:30} 
/* 背景为黄色 */ 
#map{ position:absolute;left:300px;top:0px;z-index:70} 

#charts{ position:absolute;left:800px;top:0px;z-index:70} 

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  background-image:url(background.jpg);
  background-size: cover;
}
</style>
