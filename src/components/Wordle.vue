/* eslint-disable */
<template>
  <div id="Wordle" class="Wordle" style="height:30px">
    <h4>Wordle</h4>

</div>
</template>


<script>
import * as d3 from "d3";
import * as d3Chromatic from 'd3-scale-chromatic';
import Bus from '../assets/bus.js';
export default {
  name: "App",
  data(){
    return{
      svg:undefined,
      tooltip:undefined,
      g1:undefined,
      g1_5:undefined,
      x:undefined,
      y:undefined,
      u1:undefined,
      u2:undefined,
      myColor:undefined,
      legend0:undefined,
      legend1:undefined,
      legend2:undefined,
      legend3:undefined,
      legend4:undefined,
      legend5:undefined,
      legend6:undefined,
      data_all:undefined,
      yAxis:'',
      vertices:undefined
    }
  },
  //created(){
    //Bus.$on("Map_place", (val) => {
                //this.place = val;}),
    //Bus.$on("Map_places", (val) => {
                //this.places = val;})},
  mounted() {
    this.generateWord()
    this.handle()
  },
  methods: {
    handle: function () {
    Bus.$on("Get_Predict",(val) => {this.Get_Predict(val)})
    Bus.$on("New_Poet",(val) => {this.update_chart(val)})
  },
    generateWord() {

// set the dimensions and margins of the graph
var margin = {top: 0, right: 35, bottom: 50, left: 30},
    width = 300 - margin.left - margin.right,
    height = 565 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#Wordle")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

let self = this
// Parse the Data
d3.csv("sushi_wordcount1.csv", function(data_all) {
var data = []
self.data_all = data_all
for(var i in data_all){
  if (data_all[i]['name']=='Su Shi'){
    data.push(data_all[i])
  }
}
data.sort(function(b, a) {
  return a.count - b.count;
});
var data_1 = data.slice(0,30)
var myColor = d3.scaleSequential()
    .domain([0.83,0.42])
    .interpolator(d3Chromatic.interpolatePiYG);
self.myColor = myColor


  self.legend0 = svg.append("circle").attr("cx",245).attr("cy",12+1*30).attr("r", 6).style("fill", function(){return myColor(0.42+0*(0.83-0.42)/5)})
  self.legend1 = svg.append("circle").attr("cx",245).attr("cy",12+2*30).attr("r", 6).style("fill", function(){return myColor(0.42+1*(0.83-0.42)/5)})  
  self.legend2 = svg.append("circle").attr("cx",245).attr("cy",12+3*30).attr("r", 6).style("fill", function(){return myColor(0.42+2*(0.83-0.42)/5)})
  self.legend3 = svg.append("circle").attr("cx",245).attr("cy",12+4*30).attr("r", 6).style("fill", function(){return myColor(0.42+3*(0.83-0.42)/5)})
  self.legend4 = svg.append("circle").attr("cx",245).attr("cy",12+5*30).attr("r", 6).style("fill", function(){return myColor(0.42+4*(0.83-0.42)/5)})

  svg.append("text").attr("x",219).attr("y",8)
  .text(function(){return 'Sentiment'}).style("font-size","11px")
  svg.append("text").attr("x",230).attr("y",68-1*44)
  .text(function(){return 'Score'}).style("font-size","11px")
  svg.append("text").attr("x",219).attr("y",60+0*30)
  .text(function(){return '0.42~0.50'})
    svg.append("text").attr("x",219).attr("y",60+1*30)
  .text(function(){return '0.50~0.58'})
    svg.append("text").attr("x",219).attr("y",60+2*30)
  .text(function(){return '0.58~0.66'})
    svg.append("text").attr("x",219).attr("y",60+3*30)
  .text(function(){return '0.66~0.75'})
    svg.append("text").attr("x",221).attr("y",60+4*30)
  .text(function(){return 'Over0.75'})


  self.legend5 =  svg.append("circle").attr("cx",245).attr("cy",12+6*30).attr("r", 6).style("fill", "rgb(100,149,237)")
  svg.append("text").attr("x",224).attr("y",60+5*30)
  .text('NoPoem')
  self.legend6 = svg.append('rect')
  .attr('x', 227)
  .attr('y', 230-8)
  .attr('width', 35)
  .attr('height', 20)
  .attr('stroke', 'black')
  .attr('fill', '#FFFFFF')
  .on("click",function(){return Bus.$emit("hover_period", 6)})
  svg.append("text").attr("x",238).attr("y",236)
  .text('All')
  self.legend0.on("click",function(){self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-select_color-position',d3.mouse(this),0,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  self.GLOBAL.Old_time = self.GLOBAL.New_time }
  return Bus.$emit("hover_period", 0)})
  //self.legend0.on("mouseout",function(){return Bus.$emit("hover_period", 6)})

  self.legend1.on("click",function(){self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-select_color-position',d3.mouse(this),1,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  self.GLOBAL.Old_time = self.GLOBAL.New_time }
  return Bus.$emit("hover_period", 1)})
  //self.legend1.on("mouseout",function(){return Bus.$emit("hover_period", 6)})
  self.legend2.on("click",function(){self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-select_color-position',d3.mouse(this),2,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  self.GLOBAL.Old_time = self.GLOBAL.New_time }
  return Bus.$emit("hover_period", 2)})
  //self.legend2.on("mouseout",function(){return Bus.$emit("hover_period", 6)})
  self.legend3.on("click",function(){self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-select_color-position',d3.mouse(this),3,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  self.GLOBAL.Old_time = self.GLOBAL.New_time }
  return Bus.$emit("hover_period", 3)})
  //self.legend3.on("mouseout",function(){return Bus.$emit("hover_period", 6)})
  self.legend4.on("click",function(){self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-select_color-position',d3.mouse(this),4,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  self.GLOBAL.Old_time = self.GLOBAL.New_time }
  return Bus.$emit("hover_period", 4)})
  //self.legend4.on("mouseout",function(){return Bus.$emit("hover_period", 6)})
  self.legend5.on("click",function(){self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-select_color-position',d3.mouse(this),5,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  self.GLOBAL.Old_time = self.GLOBAL.New_time }
  return Bus.$emit("hover_period", 5)})
  //self.legend5.on("mouseout",function(){return Bus.$emit("hover_period", 6)})
// Add X axis
var g1_5 = svg.append("g").attr("id","for_interaction_suggestion"); 
// Circles
self.g1_5 = g1_5
var g1 = svg.append("g")
var x = d3.scaleLinear()
  .domain([0, 250])
  .range([ 0, width]);
g1.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

// Y axis
var y = d3.scaleBand()
  .range([ 0, height ])
  .domain(data_1.map(function(d) { return d.word; }))
  .padding(1);
self.yAxis = g1.append("g")
  .transition()
  .duration(1000)
  .call(d3.axisLeft(y))
// Lines
var u1 = g1.selectAll("myline")
  .data(data_1)
  .enter()
  .append("line")
    .attr("x1", function(d) { return x(d.count); })
    .attr("x2", x(0))
    .attr("y1", function(d) { return y(d.word); })
    .attr("y2", function(d) { return y(d.word); })
    .attr("stroke", "grey")

var u2 = g1.selectAll("mycircle")
  .data(data_1)
  .enter()
  .append("circle")
    .attr("cx", function(d) { return x(d.count); })
    .attr("cy", function(d) { return y(d.word); })
    .attr("r", "7")
    .style("fill", function(d) { 
                var value = d.senti ;
        return myColor(value); })
    //.style("fill", "#6495ED")
    .attr("stroke", "black")
    .on("mouseover", function(d){return mouseover(d)})
    .on("mousemove", function(d){return tooltip.style("top",
    (d3.event.pageY-150)+"px").style("left",(d3.event.pageX-0)+"px").attr("data-html", "true").html('Word:'+d.word+'<br/>'+'Count:'+d.count+'  Poet:'+d.name+'<br/>'+'Senti:'+d.senti)})
    .on("mouseout", function(){return tooltip.style("visibility", "hidden")})
self.svg = svg
self.x = x
self.y = y
self.u1 = u1
self.u2 = u2
self.g1 = g1
var se = []
i = 0
var vertices = []
for (var len = data_1.length; i < len; i++) {
  var d = data_1[i]
  se.push({'coordinates':[x(d.count),y(d.word)],'color':myColor(d.senti)})
  vertices.push([x(d.count),y(d.word)])
}
self.vertices = vertices
self.GLOBAL.Wordle_state = se
self.GLOBAL.Visual_state['Wordle']['overall'] = se
//Bus.$emit("change", self.GLOBAL.Visual_state)
function mouseover(d){
  tooltip.style("visibility", "visible")
  .html('Word:'+d.word+'<br/>'+'Count:'+d.count+'  Poet:'+d.name+'<br/>'+'Senti:'+d.senti)
  self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Visual_state['Wordle']['visit'].push(d)
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-position',[x(d.count),y(d.word)],d.word,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  Bus.$emit("change", self.GLOBAL.Visual_state)
  self.GLOBAL.Old_time = self.GLOBAL.New_time
}}    
});

var tooltip = d3.select("#Wordle")
    .append("div")
    .style("width",'100px')
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
     .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "10px")
this.tooltip = tooltip
//let self = this
},
update_chart(author){
this.g1_5.selectAll("*").remove()
var myColor = this.myColor
var data_all = this.data_all
var data = []

for(var i in data_all){
  if (data_all[i]['name']==author){
    data.push(data_all[i])
  }
}
data.sort(function(b, a) {
  return a.count - b.count;
});

var data_1 = data.slice(0,30)
console.log('data_1',data_1)
var x = this.x
var y = this.y
var se = []
i = 0
for (var len = data_1.length; i < len; i++) {
  var d = data_1[i]
  se.push({'coordinates':[x(d.count),y(d.word)],'color':myColor(d.senti)})
}
this.GLOBAL.Wordle_state = se
this.GLOBAL.Visual_state['Wordle']['overall'] = se
// Y axis
y.domain(data_1.map(function(d) { return d.word; }))

this.y = y
var g1 = this.g1
g1.selectAll("*").remove();
g1.append("g")
  .attr("transform", "translate(0," + 530 + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");
this.yAxis = g1.append("g")
        .transition()
        .duration(1000)
        .call(d3.axisLeft(y))


var tooltip = this.tooltip
// Lines
this.u1 = g1.selectAll("myline")
  .data(data_1)
  .enter()
  .append("line")
  .merge(this.u1)
    .attr("x1", function(d) { return x(d.count); })
    .attr("x2", x(0))
    .attr("y1", function(d) { return y(d.word); })
    .attr("y2", function(d) { return y(d.word); })
    .attr("stroke", "grey")
this.u2 = g1.selectAll("mycircle")
  .data(data_1)
  .enter()
  .append("circle")
  .merge(this.u2)
    .attr("cx", function(d) { return x(d.count); })
    .attr("cy", function(d) { return y(d.word); })
    .attr("r", "7")
    .style("fill", function(d) { 
                var value = d.senti ;
        return myColor(value); })
    //.style("fill", "#6495ED")
    .attr("stroke", "black")
    .on("mouseover", function(d){return mouseover(d)})
    .on("mousemove", function(d){return tooltip.style("top",
    (d3.event.pageY-150)+"px").style("left",(d3.event.pageX-0)+"px").attr("data-html", "true").html('Word:'+d.word+'<br/>'+'Count:'+d.count+'  Poet:'+d.name+'<br/>'+'Senti:'+d.senti)})
    .on("mouseout", function(){return tooltip.style("visibility", "hidden")})

se = []
i = 0
var vertices = []
for (len = data_1.length; i < len; i++) {
  d = data_1[i]
  se.push({'coordinates':[x(d.count),y(d.word)],'color':myColor(d.senti)})
  vertices.push([x(d.count),y(d.word)])
}
this.vertices = vertices
this.GLOBAL.Wordle_state = se
this.GLOBAL.Visual_state['Wordle']['overall'] = se
//Bus.$emit("change", self.GLOBAL.Visual_state)
let self = this
function mouseover(d){
  tooltip.style("visibility", "visible")
  .html('Word:'+d.word+'<br/>'+'Count:'+d.count+'  Poet:'+d.name+'<br/>'+'Senti:'+d.senti)
  self.GLOBAL.New_time = new Date().getTime()/1000
  if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
  self.GLOBAL.Visual_state['Wordle']['visit'].push(d)
  self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-wordle-position',[x(d.count),y(d.word)],d.word,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file})
  Bus.$emit("change", self.GLOBAL.Visual_state)
  self.GLOBAL.Old_time = self.GLOBAL.New_time
}} 
},
Get_Predict(predict_all){
  this.g1_5.selectAll("*").remove()
  for(i in predict_all){
    var predict = predict_all[i]
  var position = predict['Behavior']
  if(predict['type']=='Click'){
    if(predict['Object_View']=='Wordle'){
      var x_position = position['x_position']
      var y_position = position['y_position']
      console.log(x_position,y_position)
      var dist = 0
      var min_dist = Number.POSITIVE_INFINITY
      var diss = 0
      for(var i in this.vertices){
        var d = this.vertices[i]
        dist = (x_position-d[0])**2+(y_position-d[1])**2
        if (dist<min_dist){
          diss = d
          min_dist = dist
        }
      }
      this.g1_5.append('circle')
    .attr('cx', diss[0])
    .attr('cy', diss[1])
    .attr('r', 12)
    .attr('fill', 'black')
    .attr("opacity",1);
  }}

  }

}
}
}

</script>