/* eslint-disable */
<template>
<div id="txt"> 
<br />
<button id="test">Save</button>
<p> </p>
</div>
</template>

<script>
//import * as d3 from "d3";
//import Bus from '../assets/bus.js';



export default {
  name: "App",
  data(){
    return{
      serverResponse: 'resp'
    }
  },
  //created(){
    //Bus.$on("Map_place", (val) => {
                //this.place = val;}),
    //Bus.$on("Map_places", (val) => {
                //this.places = val;})},
  mounted() {
    this.download()
  },
  methods: {
download() {
let self = this
function download_txt() {
  var textToSave = self.GLOBAL.Log_file
  var textToSave2 = JSON.stringify(self.GLOBAL.Visual_state_All)
  console.log(textToSave)
  var hiddenElement = document.createElement('a');

  hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave)+ encodeURI(textToSave2);
  hiddenElement.target = '_blank';
  hiddenElement.download = 'Please_send_the_file_to_yixuan.txt';
  hiddenElement.click();
}

document.getElementById('test').addEventListener('click', download_txt);
},
getData(){
this.getMsg()
this.postInteraction({'name':this.GLOBAL.Log_file})
}}}

</script>