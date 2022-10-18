/* eslint-disable */s
<template>
  <div id="force">
    <p>
      <h4>  Places connection</h4>
  </div>
</template>

<script>
import * as d3 from "d3";
//import * as topojson from "topojson"
import Bus from '../assets/bus.js';

export default {
  name: "App",
  data(){
    return{
      data:undefined,
      place:[],
      all_places:{},
      svg2:undefined,
      width2 :undefined,
      height2 : undefined,
      Hist_select_data:'',
      nodeElements:undefined,
      vertices:''
    }
  },
  mounted() {
    this.handle()
  },
  methods: {
    handle: function () {
    Bus.$on("Start_Place", () => {
                this.generateForce()
              }),  
    Bus.$on("Map_select_data", (val) => {
                this.data = val
                this.updateForce()
              }),
    Bus.$on("Hist_select_data", (val) => {
                this.Hist_select_data = val
                this.select_new_point()
              })
    Bus.$on("Get_Predict",(val) => {this.Get_Predict(val)})
  },
    generateForce() {
var data_place = []
var width2 = 400,
    height2 = 285;
this.width2 = width2
this.height2 = height2
const svg2 = d3.select("#force").append("svg")

  svg2.attr("width", width2)
    .attr("height", height2);

// center marker
svg2.append('circle')
    .attr('r', 3)
    .attr('cx', width2 / 2)
    .attr('cy', height2 / 2);
this.svg2 = svg2
let self = this
/*
d3.json("sushi_map.json", function(error, point) {
  const places_all = topojson.feature(point, point.objects.places)
*/
var places_all = self.GLOBAL.place_now
var nodes = []
var links=[]
    for(var i=0, len=data_place.length;i<len;i++){
        nodes.push({"name":data_place[i]})
      }
    for(i=1, len=places_all.features.length-1; i<len; i++){
    // (note: loop until length - 1 since we're getting the next
    //  item with i+1)
    var place1 = places_all.features[i].properties.name.toString()
    var place2 = places_all.features[i+1].properties.name.toString()
    // if ((place1 in data)&&(place2 in data)){
    var a = check_in(data_place, place1)
    var b = check_in(data_place, place2)
    if((a=="TRUE") && (b=="TRUE")){
      var index1 = data_place.findIndex(check_equal1)
      var index2 = data_place.findIndex(check_equal2)
      links.push({"source": index1, "target": index2})
    }
}
function check_equal1(place){return place.toString()==place1}
function check_equal2(place){return place.toString()==place2}
function check_in(data, place){
  for(var i=0, len=places_all.features.length-1; i<len; i++){
    var d = data[i]
    if(d== place){
      return 'TRUE'
    }}
  return 'False'
}
var linkElements = svg2.selectAll()
        .data(links)
        .enter()
        .append('line')
        .attr('stroke', 'black')
        .attr('stroke-width', '2px');
self.nodeElements = svg2.selectAll()
        .data(nodes)
        .enter()
        .append('circle')
        .attr('r', 5)
        .attr('fill', 'red')

var textElements = svg2.selectAll()
  .data(nodes)
  .enter().append('text')
    .text(node => node.name)
    .attr('font-size', 15)
    .attr('dx', 15)
    .attr('dy', 4)
const simulation = d3.forceSimulation()
          .force('link', d3.forceLink().distance(80))
          .force('charge', d3.forceManyBody())
          .force('center', d3.forceCenter(width2 / 2, height2 / 2));

simulation
    .nodes(nodes)
    .on('tick', () => {
  linkElements
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
  self.nodeElements
    .attr('cx', node => node.x)
    .attr('cy', node => node.y)
  textElements
    .attr('x', node => node.x)
    .attr('y', node => node.y)
})

simulation
    .force('link')
    .links(links);
/*
function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}
*/
},
updateForce(){

  let self = this
function unique(arr) {
    return arr.filter(function(item, index, arr) {
      // 取出元素, 该元素在数组中第一次出现的索引 === 当前索引值
      return arr.indexOf(item, 0) === index;
    });
}
function countTimes(data) {
    return data.reduce(function(time, name) {
        if (name in time) {
            time[name]++;
        } else {
            time[name] = 1;
        }
        return time;
    }, {});
}

var data_select = []
var data_select1 = []
var place_count = []
for(var i=0, len=this.data.length-1; i<len; i++){
  var d = this.data[i]
  data_select1.push(d.properties.name.toString())}
  data_select = unique(data_select1)
  place_count = countTimes(data_select1)
var max_count = 0
for(i in place_count){
  var item = place_count[i];
  if (item>max_count){
    max_count = item
  }
}
  var height2 = this.height2
  var width2 = this.width2
  var svg2 = this.svg2
  var places_all = self.GLOBAL.place_now
  svg2.selectAll("*").remove();
  this.g1_5 = svg2.append("g").attr("id","for_interaction_suggestion"); 
  svg2.append('circle')
    .attr('r', 5)
    .attr('cx', width2 / 2)
    .attr('cy', height2 / 2);
var nodes = []
var links=[]
    for(i=0, len=data_select.length;i<len;i++){
        nodes.push({"name":data_select[i]})
      }
    for(i=1, len=places_all.features.length-1; i<len; i++){
    // (note: loop until length - 1 since we're getting the next
    //  item with i+1)
    var place1 = places_all.features[i].properties.name.toString()
    var place2 = places_all.features[i+1].properties.name.toString()
    // if ((place1 in data)&&(place2 in data)){
    var a = check_in(data_select, place1)
    var b = check_in(data_select, place2)
    if((a=="TRUE") && (b=="TRUE")){
      var index1 = data_select.findIndex(check_equal1)
      var index2 = data_select.findIndex(check_equal2)
      links.push({"source": index1, "target": index2})
    }}
function check_in(data, place){
  for(var i=0, len=places_all.features.length-1; i<len; i++){
    var d = data[i]
    if(d== place){
      return 'TRUE'
    }}
  return 'False'
}
var visited = []
//var select_place_from_force = []
var linkElements = svg2.selectAll()
        .data(links)
        .enter()
        .append('line')
        .attr('stroke', 'black')
        .attr('stroke-width', '2px');
self.nodeElements = svg2.selectAll()
        .data(nodes)
        .enter()
        .append('circle')
        .attr('r', function(node){return 8*(place_count[node.name]+4)/(5+max_count)})
        .attr('id', function(node){return node.name})
        .attr('fill', '#6495ED')
        .on('mouseover',function(){var that = this
          d3.select(that).attr("fill",'orange')
          self.GLOBAL.New_time = new Date().getTime()/1000
          if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
          visited.push(that)
          self.GLOBAL.Visual_state['Force']['visited'] = visited
          Bus.$emit("change", self.GLOBAL.Visual_state)
          self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-force-position',d3.mouse(this),that.id,'\n'])
          self.postInteraction({'name':self.GLOBAL.Log_file})
          self.GLOBAL.Old_time = self.GLOBAL.New_time}
          Bus.$emit("Force_select_data", that.id)})
        .on('mouseout', function(){return self.nodeElements.attr('fill', '#6495ED')})


var textElements = svg2.selectAll()
  .data(nodes)
  .enter().append('text')
    .text(node => node.name)
    .attr('font-size', 13)
    .attr('dx', 8)
    .attr('dy', 4)

const simulation = d3.forceSimulation()
          .force('link', d3.forceLink().distance(50))
          .force('charge', d3.forceManyBody(-100))
          .force('center', d3.forceCenter(width2 / 2, height2 / 2));
Bus.$emit('Brush_update','start')
simulation
    .nodes(nodes)
    .on('tick', () => {
  linkElements
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
  self.nodeElements
    .attr('cx', function(d){return d.x = Math.max(5,Math.min(self.width2-4,d.x))})
    .attr('cy', function(d){return d.y = Math.max(5,Math.min(self.height2-4,d.y))})
  textElements
    .attr('x', node => node.x)
    .attr('y', node => node.y)
})
    .on('end',() => {
      visited = []
      var se = []
      var vertices = []
for (i = 0, len = nodes.length; i < len; i++) {
  var d =nodes[i]
  se.push({'coordinates':[d.x,d.y],'r':8*(place_count[d.name]+4)/(5+max_count),'name':d.name})
  vertices.push([d.x,d.y])
}
self.vertices = vertices
Bus.$emit('Brush_update','finsih')
self.GLOBAL.Force_state.push({'Force':se})
self.GLOBAL.Visual_state['Force']['overall'] = se
self.GLOBAL.Visual_state['Force']['visit'] = []
Bus.$emit("change", self.GLOBAL.Visual_state)
    })

simulation
    .force('link')
    .links(links);


/*
console.log(nodes[1])
console.log(self.nodeElements)
var se = []
for (i = 0, len = self.nodeElements._groups.length; i < len; i++) {
  var d =self.nodeElements._groups[0][i].__data__
  console.log(i,d,d.x,d.id)
  se.push({'coordinates':[d.x,d.y],'r':8*(place_count[d.name]+4)/(5+max_count),'name':d.name})
}
self.GLOBAL.Visual_state.push({'Force':se})
console.log(self.GLOBAL.Visual_state)

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}
*/
function check_equal1(place){return place.toString()==place1}
function check_equal2(place){return place.toString()==place2}
},
select_new_point(){
  var data = this.Hist_select_data
  this.nodeElements.attr('fill',function(d){return isSelectedByHist(d,data)
function isSelectedByHist(a,data){
  for(var i=0,len=data.length;i<len;i++){
    var place = data[i].properties.name
      if(a.name==place){
        return 'orange'}
    }
    return "#6495ED"
  }

})
},
Get_Predict(predict_all){
  Bus.$on('Brush_update',(val) => {
    if(val=='finsih'){
  this.g1_5.selectAll("*").remove()
  for(var i in predict_all){
    var predict = predict_all[i]
    var position = predict['Behavior']
    if (predict['type']=='Click'){
    if(predict['Object_View']=='Force'){
    var x_position = position['x_position']
    var y_position = position['y_position']
    var dist = 0
    var min_dist = Number.POSITIVE_INFINITY
    var diss = 0
    for(i in this.vertices){
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
  .attr('r', 10)
  .attr('fill','red')
  .attr("opacity",1);}}
}

    }
  }),
  Bus.$on('Force_select_data',() => { 
  this.g1_5.selectAll("*").remove()
  for(var i in predict_all){
    var predict = predict_all[i]
    var position = predict['Behavior']
    if (predict['type']=='Click'){
    if(predict['Object_View']=='Force'){
    var x_position = position['x_position']
    var y_position = position['y_position']
    var dist = 0
    var min_dist = Number.POSITIVE_INFINITY
    var diss = 0
    for(i in this.vertices){
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
  .attr('r', 10)
  .attr('fill','red')
  .attr("opacity",1);}}
}

  }

  )
}
}
}
</script>

<style>

.selected{
  fill: yellow;
}