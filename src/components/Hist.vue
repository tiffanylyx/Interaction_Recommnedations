/* eslint-disable */
<template>
  <div id="hist">
     <p>
      <h4>  Distribution of visit against age</h4>
  </div>
</template>

<script>
import * as d3 from "d3";
import Bus from '../assets/bus.js';

export default {
  name: "App",
  data(){
    return{
      data:undefined,
      svg:undefined,
      x:undefined,
      y:undefined,
      yAxis:undefined,
      u:undefined,
      height1:undefined,
      select_data_from_hist:undefined,
      g1_5:undefined,
      vertices:''
    }
  },
  created(){
    Bus.$on("Map_select_data", (val) => {
                this.data = val;}),
    Bus.$on("New_Poet", (val) => {
                this.update_over_hist(val);})
  },
  mounted() {
    this.generateHist();
    this.handle()
  },
  //watch:{handle(newval){
    //this.age=newval,
    //this.generateHist()}},
  methods: {
    handle: function () {
    Bus.$on("Map_select_data", (val) => {
                this.data = val;
                this.updatehist()
              })
    Bus.$on("Get_Predict",(val) => {this.Get_Predict(val)})},
    generateHist() {
      //let age = this.$root.age_select
      var min = 18;
      var max = 68;
      var domain = [min,max];
      var a = [19,19,20,20,20,20,20,20,20,20,20,20,20,20,20,20,21,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,24,24,24,24,24,24,24,24,24,24,25,25,25,25,25,25,26,26,26,26,26,26,26,26,26,26,26,26,26,27,27,27,27,27,27,27,27,27,27,27,27,27,27,28,28,28,28,28,28,28,28,28,28,28,28,29,29,29,29,29,30,30,30,30,30,31,31,31,31,31,31,31,31,32,32,32,32,32,32,32,32,33,35,35,35,35,35,35,35,35,35,35,35,35,35,35,36,36,36,36,36,36,36,36,36,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,41,41,41,41,41,41,41,41,41,41,41,42,42,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,45,45,45,45,45,45,45,45,45,45,45,45,46,46,46,46,46,46,46,46,46,46,47,47,47,47,47,47,47,47,47,47,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,53,53,53,53,53,53,53,53,53,53,53,53,53,55,55,55,55,55,55,55,55,55,55,55,55,56,56,56,56,56,56,56,56,56,56,57,57,57,57,57,57,57,57,57,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,59,59,59,59,61,61,61,61,61,61,61,61,61,61,62,62,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65]
      var margin = { top: 5, right: 5, bottom: 30, left: 30 },
        width1 = 400 - margin.left - margin.right
      this.height1 = 280 - margin.top - margin.bottom;
      const svg1 = d3
        .select("#hist")
        .append("svg")
        .attr("width", width1 + margin.left + margin.right)
        .attr("height", this.height1 + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var x = d3
          .scaleLinear()
          .domain(domain) 
          .range([0, width1]); 

        svg1.append("g")
          .attr("transform", "translate(0," + this.height1 + ")")
          .call(d3.axisBottom(x));
          // Y axis: initialization
        var y = d3.scaleLinear()
          .range([this.height1, 0]);
        this.yAxis = svg1.append("g")
        var nBin=20
        var histogram = d3
          .histogram()
          .domain(x.domain()) // then the domain of the graphic
          .thresholds(x.ticks(nBin)); // then the numbers of bins

        // And apply this function to data to get the bins
        var bins = histogram(a);
        // Add the svg element to the body and set the dimensions and margins of the graph

        y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
        this.yAxis
        .transition()
        .duration(1000)
        .call(d3.axisLeft(y));
        this.u = svg1
          .selectAll("rect")
          .data(bins)

        this.u.enter()
          .append("rect")
          .attr("x", 1)
          .merge(this.u)
          .transition()
          .attr("height", (d)=>this.height1 - y(d.length))
          .attr("transform", function(d) { 
            return "translate(" + x(d.x0) + "," + y(d.length) + ")"; 
          })
          .attr("width", function(d) {
            return x(d.x1) - x(d.x0) - 1})
          .attr("fill", "#6495ED")
          this.x = x
          this.y = y
          this.svg = svg1
                var g1_5 = svg1.append("g").attr("id","for_interaction_suggestion");
        this.g1_5 = g1_5}, 
update_over_hist(author){
//let self = this
//var all_data = this.data

var svg1 = this.svg
var x = this.x
var y = this.y
// The number of bins 
var nBin=20
var histogram = d3
  .histogram()
  .domain(x.domain()) // then the domain of the graphic
  .thresholds(x.ticks(nBin)); // then the numbers of bins
if(author=='Su Shi'){
var a = [19,19,20,20,20,20,20,20,20,20,20,20,20,20,20,20,21,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,24,24,24,24,24,24,24,24,24,24,25,25,25,25,25,25,26,26,26,26,26,26,26,26,26,26,26,26,26,27,27,27,27,27,27,27,27,27,27,27,27,27,27,28,28,28,28,28,28,28,28,28,28,28,28,29,29,29,29,29,30,30,30,30,30,31,31,31,31,31,31,31,31,32,32,32,32,32,32,32,32,33,35,35,35,35,35,35,35,35,35,35,35,35,35,35,36,36,36,36,36,36,36,36,36,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,41,41,41,41,41,41,41,41,41,41,41,42,42,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,45,45,45,45,45,45,45,45,45,45,45,45,46,46,46,46,46,46,46,46,46,46,47,47,47,47,47,47,47,47,47,47,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,53,53,53,53,53,53,53,53,53,53,53,53,53,55,55,55,55,55,55,55,55,55,55,55,55,56,56,56,56,56,56,56,56,56,56,57,57,57,57,57,57,57,57,57,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,59,59,59,59,61,61,61,61,61,61,61,61,61,61,62,62,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65]}
else if (author=='Huang Tingjian'){
  a = [1, 15, 19, 19, 22, 22, 23, 23, 24, 28, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 37, 37, 37, 39, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 41, 41, 41, 47, 47, 47, 49, 49, 50, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 51, 54, 54, 54, 56, 56, 56, 56, 56, 57, 57, 57, 57, 57, 57, 57, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 59, 59, 60, 60, 60, 60, 60, 60, 60, 60]}
else if (author=='Ouyang Xiu'){
  a = [1, 4, 4, 5, 6, 20, 20, 21, 21, 21, 21, 21, 21, 21, 22, 22, 24, 25, 26, 26, 26, 26, 26, 26, 26, 27, 27, 27, 27, 27, 28, 28, 28, 28, 28, 28, 29, 29, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 31, 31, 31, 31, 31, 31, 31, 32, 32, 32, 32, 33, 33, 33, 33, 34, 34, 34, 34, 36, 37, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 39, 39, 39, 39, 39, 42, 43, 43, 43, 44, 46, 47, 47, 47, 48, 48, 49, 49, 49, 49, 50, 50, 50, 61, 61, 62, 62, 62, 64, 64, 65]}
else if (author == 'Xin Qiji'){
  a = [1, 15, 16, 18, 19, 23, 25, 26, 29, 31, 33, 34, 35, 36, 38, 39, 39, 39, 39, 39, 40, 40, 41, 41, 42, 43, 47, 47, 47, 48, 52, 52, 53, 53, 54, 54, 54, 54, 54, 55, 55, 55, 55, 55, 56, 56, 56, 57, 64, 65, 65, 66, 66, 67, 68, 68]
}
console.log(a)
// And apply this function to data to get the bins
var bins = histogram(a);
// Add the svg element to the body and set the dimensions and margins of the graph
y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
this.yAxis
.transition()
.duration(1000)
.call(d3.axisLeft(y));

this.u = svg1
  .selectAll("rect")
  .data(bins)

  this.u.enter()
  .append("rect")
  .attr("x", 1)
  .merge(this.u)
  .transition()
  .attr('height', (d)=>this.height1 - y(d.length))
  .attr("transform", function(d) { 
    return "translate(" + x(d.x0) + "," + y(d.length) + ")"; 
  })
  .attr("width", function(d) {
    return x(d.x1) - x(d.x0) - 1})
  .attr("fill", "#6495ED")

},
updatehist(){
  this.g1_5.selectAll("*").remove()
let self = this
var all_data = this.data
var age = []
for(var i=0, len=this.data.length-1; i<len; i++){
  var d = this.data[i]
  age.push(parseInt(d.properties.age))}
var svg1 = this.svg
var x = this.x
var y = this.y
// The number of bins 
var nBin=20
var histogram = d3
  .histogram()
  .domain(x.domain()) // then the domain of the graphic
  .thresholds(x.ticks(nBin)); // then the numbers of bins

// And apply this function to data to get the bins
var bins = histogram(age);
// Add the svg element to the body and set the dimensions and margins of the graph
y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
this.yAxis
.transition()
.duration(1000)
.call(d3.axisLeft(y));

this.u = svg1
  .selectAll("rect")
  .data(bins)

  this.u.enter()
  .append("rect")
  .attr("x", 1)
  .merge(this.u)
  .transition()
  .attr('height', (d)=>this.height1 - y(d.length))
  .attr("transform", function(d) { 
    return "translate(" + x(d.x0) + "," + y(d.length) + ")"; 
  })
  .attr("width", function(d) {
    return x(d.x1) - x(d.x0) - 1})
  .attr("fill", "#6495ED")
  .attr("id",function(d,i){
    return [18+i*2,i]
  })
var se = []
var vertices = []
for (i = 0, len = bins.length; i < len; i++) {
  d = bins[i]
  se.push({'coordinates':[x(d.x0),y(d.length)]})
  if(y(d.length)<245){
    vertices.push(i)
  }
}
self.vertices = se
self.GLOBAL.Visual_state['Hist']['overall'] = se
self.GLOBAL.Visual_state['Hist']['visit'] = []

var select_age_by_column = []
this.u.on("click",function(){
    var that = this
    var age = that.id.split(",")[0]
    console.log('age11',that.id)
    var index = that.id.split(",")[1]
    self.GLOBAL.New_time = new Date().getTime()/1000
    if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
    self.GLOBAL.Visual_state['Hist']['visit'].push([age,index])
    Bus.$emit("change", self.GLOBAL.Visual_state['Hist'])
    self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,"click-hist-index",index,'\n'])
    self.postInteraction({'name':self.GLOBAL.Log_file})
    self.GLOBAL.Old_time = self.GLOBAL.New_time}
    select_age_by_column = parseInt(age)
    console.log('select_age_by_column',select_age_by_column)
    d3.select(that)
    .transition()
    .duration(500)
    .attr("fill", "orange");
var select_data_from_hist = []
for(i=0, len=all_data.length-1; i<len; i++){
  d = parseInt(all_data[i].properties.age)
    if(d<select_age_by_column+2){
      if (d>parseInt(select_age_by_column)-1){
      select_data_from_hist.push(all_data[i])
    }}
  }
console.log('age',select_age_by_column)
Bus.$emit("Hist_select_data", select_data_from_hist)
console.log('select_data_from_hist',select_data_from_hist)
})
this.u.on("mouseout", function(){
  d3.select(this)
    .transition()
    .duration(500)
    .attr("fill", "#6495ED");
})
},
Get_Predict(predict_all){
  
  this.g1_5.selectAll("*").remove()
  for(var i in predict_all){
    var predict = predict_all[i]
    var position = predict['Behavior']
    if (predict['type']=='Click'){
      if(predict['Object_View']=='Hist'){
        console.log('herehere')
        var number = position['number']
        console.log('number',number)
        var dist = 0
        var min_dist = Number.POSITIVE_INFINITY
        var diss = 0
        console.log('this.vertices',this.vertices)
        for(i in this.vertices){
          var d = this.vertices[i].coordinates[0]/15.234
          console.log('d',d)
          dist = (number-d)**2
          if (dist<min_dist){
            diss = this.vertices[i].coordinates
            min_dist = dist
          }
        }
        console.log('diss',diss)
        if(diss[1]!=245){
        this.g1_5.append("path")
        .attr("d", d3.symbol().type(d3.symbolStar).size(100))
        .attr("fill", "orange")
        .attr("transform","translate("+diss[0]+","+diss[1]+")")

        }

  /*
  .attr('cx', diss*15.2)
  .attr('cy', 245)
  .attr('r', 7)
  .attr('stroke', 'black')
  .attr("stroke-width",'4px')
  .attr("opacity",1)
  .attr('fill', '#69a3b2');
*/


      }

}
}
}
}}

</script>