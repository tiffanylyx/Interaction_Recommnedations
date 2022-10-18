/* eslint-disable */
<template>
  <div>
    <div style = "width:380px;height:44px;float:left">
      <h4>Footprint</h4>
    </div>
    <div id = 'pos'  style = "width:120px;height:24px;float:left">
      <p>  </p>

    </div>
  <div id="map">
  </div>
</div>
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson"
import * as d3Chromatic from 'd3-scale-chromatic';
//import Vue from 'vue';
import Bus from '../assets/bus.js';
//import * as d3Voronoi from 'd3-voronoi'
//var msgCenter = new Vue()
export default {
  name: "App",
  data() {
    return {
      place_color:'',
      select_data:'',
      Hist_select_data:'',
      Force_select_data:'',
      myCircle:'',
      myLink:'',
      svg:'',
      hover_period:'',
      g4:'',
      g3:'', 
      g2:'',
      zoom_value:[],
      g1_5:'',
      vertices:'',
      group1:'',
      g1:'',
      projection:'',
      path:'',
      dropdownButton:'',
      subunits:'',
      places:''
    };
  },
  //created() {
    // 在需要的传递数据的时候调用sendData方法，这里模拟调用
    //this.sendData();
    
  //},
  mounted() {
    this.getMap();
    this.handle()
    //this.sendData();
  },
  methods: {
    handle: function () {
    Bus.$on("subunits",()=>{this.generateArc()})
    Bus.$on("New_Poet", (val) => {
      this.update(val)}),  
    Bus.$on("hover_period", (val) => {
      this.hover_period=val;
      this.show_period()}),
    Bus.$emit("Map_age", this.select_value),
    Bus.$on("Hist_select_data", (val) => {
      this.Hist_select_data=val;
      this.select_new_point()}),
    Bus.$on("change", () => {
      var time = new Date().getTime()/1000

      this.GLOBAL.Visual_state['timestamp'] = time
      var save = JSON.stringify(this.GLOBAL.Visual_state)

      this.GLOBAL.Visual_state_All.push([time,save])
      this.postVisual({'name':this.GLOBAL.Visual_state})}),  
    Bus.$on("Force_select_data", (val) => {
      this.Force_select_data=val;
      this.select_new_point_Force()})
    Bus.$on("Get_Predict",(val) => {this.Get_Predict(val)})},
    getMap(){
      let self = this
        d3.json("sushi_map.json", function(error, point) {
        self.subunits = topojson.feature(point, point.objects.china)
        Bus.$emit("subunits",self.subunits)
})
    },
    generateArc() {
      const width = 500;
      const height = 640;

      const projection = d3.geoAlbers()
          .center([2, 29.6])
          .rotate([-110, 0])
          .parallels([20, 60])
          .translate([width / 2, height / 2])
          .scale(1600)
      this.projection = projection

      const path = d3.geoPath()
          .projection(projection)
          .pointRadius(2);
      this.path = path
      var dropdownButton = d3.select("#pos")
      .append('select').attr("x","100px")
      
      const svg = d3
        .select("#map")
        .append("svg")
        .attr("width", width)
        .attr("height", height);
      let self = this
      d3.csv("place_senti2.csv",function(data_all){
        var data = {'Su Shi':[],'Huang Tingjian':[],'Ouyang Xiu':[],'Xin Qiji':[]}
        for(var i in data_all){
          if(data_all[i]['author']=='Su Shi'){
            data['Su Shi'].push(data_all[i])
          }
          else if(data_all[i]['author']=='Huang Tingjian'){
            data['Huang Tingjian'].push(data_all[i])
          }
          else if(data_all[i]['author']=='Ouyang Xiu'){
            data['Ouyang Xiu'].push(data_all[i])
          }
          else if(data_all[i]['author']=='Xin Qiji'){
            data['Xin Qiji'].push(data_all[i])
          }          
        }
        self.place_color = data
        self.place_color_select = data['Su Shi']
      })
      d3.json("map.json", function(error, point) {
      var subunits = self.subunits
      var places_all = topojson.feature(point, point.objects.places)
      var places1 = []
      for(i in places_all['features']){
        if(places_all['features'][i].properties.author=='Su Shi'){
          places1.push(places_all['features'][i])
        }
      }
      var places = {type: "FeatureCollection",features:places1}
      self.places = places
      self.GLOBAL.place_now = places
      Bus.$emit('Start_Place', places)
  var myColor = d3.scaleSequential()
    .domain([0.83,0.42])
    .interpolator(d3Chromatic.interpolatePiYG);
  function choose_color(place){
    var name = place.properties.name
    var res = "rgb(100,149,237)"
    for (var i = 0;i<self.place_color_select.length; i++) {
      var sli = self.place_color_select[i]
      if(name == sli['place']){
        res = myColor(sli['senti'])
      }
    }
    return res
  }

  var zoom = d3.zoom()
      .scaleExtent([0.5,3])//用于设置最小和最大的缩放比例
      .on("zoom",zoomed) 
/*
self.GLOBAL.New_time = new Date().getTime()/1000
self.GLOBAL.Old_time = self.GLOBAL.New_time
self.GLOBAL.Log_file.push(['Start_timestamp',self.GLOBAL.New_time,'\n'])
self.postInteraction({'name':self.GLOBAL.Log_file})*/
//编写 平移函数
/*
function reset() {
    
      svg.transition().duration(750).call( //duration过渡时间
        zoom.transform,
        d3.zoomIdentity, //控制缩放中心的为鼠标当前位置
        d3.zoomTransform(svg.node()).invert([width / 2, height / 2]) //弹性动画的圆心位置
      );
}*/
// 缩放函数

function zoomed() {
    const transform = d3.event.transform; //识别鼠标事件
    self.GLOBAL.New_time = new Date().getTime()/1000
      self.zoom_value.push(['timestamp',new Date().getTime()/1000,'Zoom-Map-Value',transform,'\n'])
    self.GLOBAL.Old_time = self.GLOBAL.New_time
    
    group1.attr("transform", transform); //将缩放结果传给g
    var k = Math.sqrt(100 / projection.scale()); //修改地图尺寸
    group1.attr("stroke-width", 1 / k); //修改对应的属性
    return transform
}
    var group1 = svg.append("g").attr("id","group").datum({
    x: 0,
    y: 0
  })//.on("click", reset);  //定义点击事件
      var g1 = group1.append("g").attr("id","for_path"); 
      //var g0 = group.append("g").attr("id","for_vo"); //新增组，用于存储不同对象
      var g1_5 = group1.append("g").attr("id","for_interaction_suggestion"); //
      self.g1_5 = g1_5
      var g3 = group1.append("g").attr("id","for_line").attr("pointer-events","none");
      var g2 = group1.append("g").attr("id","for_circle");
self.g2 = g2
self.g3 = g3
// 


g1.selectAll(".subunit")
      .data(subunits.features)
    .enter().append("path")
      .attr("class", function(d) { return "subunit " + d.id; })
      .attr("d", path)
      .attr('stroke','#222')
      .attr('stroke-width','1px')
      .attr('fill',function(d){var p = d.properties.name
        if((p=='山西省')|(p=='陕西省')|(p=='河南省')|(p=='河北省')|(p=='北京市')|
          (p=='天津市')|(p=='河南省')|(p=='山东省')|(p=='江苏省')|(p=='浙江省')|
          (p=='上海市')|(p=='湖南省')|(p=='湖北省')|(p=='江西省')|(p=='重庆市')|
          (p=='四川省')|(p=='广西壮族自治区')|(p=='海南省')|(p=='广东省')|(p=='贵州省')|
          (p=='福建省')|(p=='安徽省')){return '#ccc'}
        else{return '#fff'}})

var link1s = [
  {type: "LineString", age:0,coordinates: [[0,0],[0,0]]}
]
    for(var i=0, len=places.features.length-1; i<len; i++){
    // (note: loop until length - 1 since we're getting the next
    //  item with i+1)
        link1s.push({
            type: "LineString",
            age : places.features[i].properties.age,
            coordinates: [
                [ places.features[i].geometry.coordinates[0], places.features[i].geometry.coordinates[1]],
                [ places.features[i+1].geometry.coordinates[0], places.features[i+1].geometry.coordinates[1]]]
        });
    }
    g3.append('svg:defs').append('svg:marker')
        .attr('id', 'end-arrow')
        .attr('viewBox', '0 -5 8 8')
        .attr('refX', 5)
        .attr('markerWidth', 2.5)//箭头参数适当按需调整
        .attr('markerHeight', 2.5)
        .attr('orient', 'auto')
        .append('svg:path')
        .attr('d', 'M0,-5L10,0L0,5')//绘制箭头形状
        .attr('fill', '#483D8B');
  // 加label

  self.myLink = g3.selectAll("myPath")

      .data(link1s)
      .enter()
      .append("path")
        .attr("d", function(d){ return path(d)})
        .style("fill", "none")
        .style("stroke", "#483D80")
        .style("stroke-width", 2)
        .style("opacity",0.4)
        .attr("marker-end", "url(#end-arrow)")
      g3.append("path")
        .attr("d", d3.symbol().type(d3.symbolStar).size(200))
        .attr("fill",'red')
        .attr("transform","translate(297,166)")
  self.myCircle = g2.selectAll(".place-point")
      .data(places.features)
    .enter()
    .append("circle")
      .attr("class", "place-point")
      .attr("transform", function(d) { return "translate(" + projection(d.geometry.coordinates) + ")"; })
      .attr("x", function(d) { return d.geometry.coordinates[0] > -1 ? 6 : -6; })
      .attr("dy", ".35em")
      .attr("r", 4.8)//function(d) { return d.properties.age/10; })
      .attr("fill", function(d){return choose_color(d)})
      .attr("opacity",0.7)


  self.svg = svg
  var se = []
  var vertices = []
for (i = 0, len = places.features.length; i < len; i++) {
  var d = places.features[i]
  se.push({'coordinates':projection(d.geometry.coordinates),'color':choose_color(d)})
  vertices.push(projection(d.geometry.coordinates))
}
self.vertices = vertices
self.GLOBAL.Visual_state['Map']['overall'] = se

var allGroup = ['none',"select area", "zoom", "show point info"]
dropdownButton.on("change", dropchange)

// add the options to the button
dropdownButton // Add a button
  .selectAll('myOptions') // Next 4 lines add 6 options = 6 colors
  .data(allGroup)
  .enter()
  .append('option')
  .text(function (d) { return d; }) // text showed in the menu
  .attr("value", function (d) { return d; }) 
self.dropdownButton = dropdownButton
var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "100")
    .style("visibility", "hidden")
var g4 = group1.append("g").attr("id","for_brush"); //

self.g4 = g4
function dropchange(){
  var newCereal = d3.select(this).property('value')
  if (newCereal=='zoom'){
    self.zoom_value = []
    svg.call(zoom)
     g4.style("display","none")
self.svg.on("click", function(){self.GLOBAL.Log_file.push(self.zoom_value[self.zoom_value.length - 1])
    self.postInteraction({'name':self.GLOBAL.Log_file})})
  self.myCircle.on("mouseover", function(){return null})
    .on("mousemove", function(){return null})
    .on("mouseout", function(){return null})
    d3.select("#map")
    .on('mouseover', function(){return null})
  }
  else if (newCereal=='select area'){
    svg.on('.zoom', null)

    g4.style("display","block")
  g4
    .call( d3.brush()                 // Add the brush feature using the d3.brush function
      .extent( [ [0,0], [width,height] ] ) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
      .on("end", updata_chart)
    )    
  }
  else if ((newCereal=='show point info'))
    {svg.on('.zoom', null)
  self.myCircle//.attr("fill", function(d){return choose_color(d)})
      .attr("opacity",0.7)
      .attr('r',4.8)
      .attr('stroke',null)

      g4.style("display","none")
    /*
    self.GLOBAL.Log_file.push(self.zoom_value[self.zoom_value.length - 1])
    console.log(self.zoom_value[self.zoom_value.length - 1])
    self.postInteraction({'name':self.GLOBAL.Log_file})
    */

      self.myCircle.on("click", function(d){d3.select(this).attr("fill","#BC8F8F")
      self.GLOBAL.New_time = new Date().getTime()/1000
      if ((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
      self.GLOBAL.Visual_state['Map']['visit'].push(d),
      Bus.$emit("change", self.GLOBAL.Visual_state),
      d3.select("#map")
  .on('click', function(){self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-map-position',d3.mouse(this),d.properties.name,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file}), self.GLOBAL.Old_time = self.GLOBAL.New_time})

  }
  return tooltip.style("visibility", "visible").style("top",(d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px").text(d.properties.name+','+d.properties.age+'岁')
})
    .on("mouseout", function(){return tooltip.style("visibility", "hidden"),d3.select(this).transition().duration(500).attr("fill", function(d){return choose_color(d)});})
    }
}

  function updata_chart(){
    self.myCircle.attr("opacity",0.7)
    self.myLink.style("opacity",0.4)
    var select_data = update_data()
  Bus.$emit("Map_select_data", select_data)
  }

  function update_data() {
    var select_data = []
    var extent = d3.event.selection
    self.myCircle.attr("fill", function(d){return choose_color(d)})
    self.myCircle.classed("selected_first", function(d){ return isBrushed(extent, projection(d.geometry.coordinates)[0],projection(d.geometry.coordinates)[1]) }) 
    self.GLOBAL.New_time = new Date().getTime()/1000
    if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
    self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'Brush-Map-Position',extent[0],extent[1],'\n'])
    self.postInteraction({'name':self.GLOBAL.Log_file})
    self.GLOBAL.Old_time = self.GLOBAL.New_time
    //console.log('r',self.GLOBAL.Get_message)
    for(i=0, len=self.places.features.length-1; i<len; i++){
      var d = self.places.features[i]
      if(isBrushed(extent, projection(d.geometry.coordinates)[0],projection(d.geometry.coordinates)[1]))
        {//a = a+parseInt(d.properties.age)}
        select_data.push(d)}
      }
      return select_data
      }

function isBrushed(brush_coords, cx, cy) {
       var x0 = brush_coords[0][0],
           x1 = brush_coords[1][0],
           y0 = brush_coords[0][1],
           y1 = brush_coords[1][1];
      return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;    // This return TRUE or FALSE depending on if the points is in the selected area
  }

  }})},
update(author){
this.g1_5.selectAll("*").remove()
this.g2.selectAll("*").remove()
this.g3.selectAll("*").remove()
this.place_color_select = this.place_color[author]
      //const width = 500;
      //const height = 640;
var svg = this.svg
var projection = this.projection 
var path = this.path
//var dropdownButton = this. dropdownButton
let self = this
      d3.json("map.json", function(error, point) {
      var places_all = topojson.feature(point, point.objects.places)

      var places1 = []
      for(i in places_all['features']){
        if(places_all['features'][i].properties.author==author){
          places1.push(places_all['features'][i])
        }
      }
      var places = {type: "FeatureCollection",features:places1}
      self.places = places
      self.GLOBAL.place_now = places
      
  var myColor = d3.scaleSequential()
    .domain([0.83,0.42])
    .interpolator(d3Chromatic.interpolatePiYG);
  function choose_color(place){
    var name = place.properties.name
    var res = "rgb(100,149,237)"
    for (var i = 0;i<self.place_color_select.length; i++) {
      var sli = self.place_color[author][i]
      if(name == sli['place']){
        res = myColor(sli['senti'])
      }
    }
    return res
  }

      var g3 = self.g3
      var g2 = self.g2

// 
var link1s = [
  {type: "LineString", age:0,coordinates: [[0,0],[0,0]]}
]
    for(var i=0, len=places.features.length-1; i<len; i++){
    // (note: loop until length - 1 since we're getting the next
    //  item with i+1)
        link1s.push({
            type: "LineString",
            age : places.features[i].properties.age,
            coordinates: [
                [ places.features[i].geometry.coordinates[0], places.features[i].geometry.coordinates[1]],
                [ places.features[i+1].geometry.coordinates[0], places.features[i+1].geometry.coordinates[1]]]
        });
    }
    g3.append('svg:defs').append('svg:marker')
        .attr('id', 'end-arrow')
        .attr('viewBox', '0 -5 8 8')
        .attr('refX', 5)
        .attr('markerWidth', 2.5)//箭头参数适当按需调整
        .attr('markerHeight', 2.5)
        .attr('orient', 'auto')
        .append('svg:path')
        .attr('d', 'M0,-5L10,0L0,5')//绘制箭头形状
        .attr('fill', '#483D8B');
  // 加label

  self.myLink = g3.selectAll("myPath")
      .data(link1s)
      .enter()
      .append("path")
        .attr("d", function(d){ return path(d)})
        .style("fill", "none")
        .style("stroke", "#483D80")
        .style("stroke-width", 2)
        .style("opacity",0.4)
        .attr("marker-end", "url(#end-arrow)")
      g3.append("path")
        .attr("d", d3.symbol().type(d3.symbolStar).size(200))
        .attr("fill",'red')
        .attr("transform","translate(297,166)")
  self.myCircle = g2.selectAll(".place-point")
      .data(places.features)
    .enter()
    .append("circle")
      .attr("class", "place-point")
      .attr("transform", function(d) { return "translate(" + projection(d.geometry.coordinates) + ")"; })
      .attr("x", function(d) { return d.geometry.coordinates[0] > -1 ? 6 : -6; })
      .attr("dy", ".35em")
      .attr("r", 4.8)//function(d) { return d.properties.age/10; })
      .attr("fill", function(d){return choose_color(d)})
      .attr("opacity",0.7)


  self.svg = svg
  var se = []
  var vertices = []
for (i = 0, len = places.features.length; i < len; i++) {
  var d = places.features[i]
  se.push({'coordinates':projection(d.geometry.coordinates),'color':choose_color(d)})
  vertices.push(projection(d.geometry.coordinates))
}
self.vertices = vertices
self.GLOBAL.Visual_state['Map']['overall'] = se})

/*
var allGroup = ['none',"select area", "zoom", "show point info"]
dropdownButton.on("change", dropchange)

// add the options to the button
dropdownButton // Add a button
  .selectAll('myOptions') // Next 4 lines add 6 options = 6 colors
  .data(allGroup)
  .enter()
  .append('option')
  .text(function (d) { return d; }) // text showed in the menu
  .attr("value", function (d) { return d; }) 

var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "100")
    .style("visibility", "hidden")
var g4 = self.g4
self.g4 = g4

function dropchange(){
  var newCereal = d3.select(this).property('value')
  if (newCereal=='zoom'){
    self.zoom_value = []
    svg.call(zoom)
     g4.style("display","none")
self.svg.on("click", function(){self.GLOBAL.Log_file.push(self.zoom_value[self.zoom_value.length - 1])
    console.log(self.zoom_value[self.zoom_value.length - 1])
    self.postInteraction({'name':self.GLOBAL.Log_file})})
  self.myCircle.on("mouseover", function(){return null})
    .on("mousemove", function(){return null})
    .on("mouseout", function(){return null})
    d3.select("#map")
    .on('mouseover', function(){return null})
  }
  else if (newCereal=='select area'){
    svg.on('.zoom', null)
    

    g4.style("display","block")
  g4
    .call( d3.brush()                 // Add the brush feature using the d3.brush function
      .extent( [ [0,0], [width,height] ] ) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
      .on("end", updata_chart)
    )    
  }
  else if ((newCereal=='show point info'))
    {svg.on('.zoom', null)
      g4.style("display","none")
    self.GLOBAL.Log_file.push(self.zoom_value[self.zoom_value.length - 1])
    console.log(self.zoom_value[self.zoom_value.length - 1])
    self.postInteraction({'name':self.GLOBAL.Log_file})


      self.myCircle.on("click", function(d){d3.select(this).attr("fill","#BC8F8F")
      self.GLOBAL.New_time = new Date().getTime()/1000
      if ((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
      self.GLOBAL.Visual_state['Map']['visit'].push(d),
      Bus.$emit("change", self.GLOBAL.Visual_state),
      d3.select("#map")
  .on('click', function(){self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'hover-map-position',d3.mouse(this),d.properties.name,'\n']),self.postInteraction({'name':self.GLOBAL.Log_file}), self.GLOBAL.Old_time = self.GLOBAL.New_time})

  }
  return tooltip.style("visibility", "visible").style("top",(d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px").text(d.properties.name+','+d.properties.age+'岁')
})
    .on("mouseout", function(){return tooltip.style("visibility", "hidden"),d3.select(this).transition().duration(500).attr("fill", function(d){return choose_color(d)});})
    }
}

  function updata_chart(){
    self.myCircle.attr("opacity",0.7)
    self.myLink.style("opacity",0.4)
    var select_data = update_data()
  Bus.$emit("Map_select_data", select_data)
  }

  function update_data() {
    var select_data = []
    var extent = d3.event.selection
    self.myCircle.attr("fill", function(d){return choose_color(d)})
    self.myCircle.classed("selected_first", function(d){ return isBrushed(extent, projection(d.geometry.coordinates)[0],projection(d.geometry.coordinates)[1]) }) 
    self.GLOBAL.New_time = new Date().getTime()/1000
    if((self.GLOBAL.New_time-self.GLOBAL.Old_time)>1){
    self.GLOBAL.Log_file.push(['timestamp',self.GLOBAL.New_time,'Brush-Map-Position',extent[0],extent[1],'\n'])
    self.postInteraction({'name':self.GLOBAL.Log_file})
    self.GLOBAL.Old_time = self.GLOBAL.New_time
    //console.log('r',self.GLOBAL.Get_message)
    for(i=0, len=places.features.length-1; i<len; i++){
      var d = places.features[i]
      if(isBrushed(extent, projection(d.geometry.coordinates)[0],projection(d.geometry.coordinates)[1]))
        {//a = a+parseInt(d.properties.age)}
        select_data.push(d)}
      }
      return select_data
      }

function isBrushed(brush_coords, cx, cy) {
       var x0 = brush_coords[0][0],
           x1 = brush_coords[1][0],
           y0 = brush_coords[0][1],
           y1 = brush_coords[1][1];
      return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;    // This return TRUE or FALSE depending on if the points is in the selected area
  }

  }})
*/},

select_new_point(){
    var data = this.Hist_select_data
    this.myCircle.classed("selected_second", function(d){return isSelectedByHist(d,data)})
    //this.myLink.style("stroke",function(d) {return LinkisSelectedByHist(d)})
    //this.myLink.style("opacity",function(d) {return LinkisSelectedByHist_O(d)})
    //this.myLink.style("stroke-width",function(d) {return LinkisSelectedByHist_S(d)})
    
function isSelectedByHist(a,data){
  for(var i=0,len=data.length;i<len;i++){
    var geo = data[i].properties.name
    var age_select = data[i].properties.age
    if (a.properties.name==geo){
      if(a.properties.age==age_select){
        return (1==1)
      }}}
  return (1==0)}
},
select_new_point_Force(){
  var data = this.Force_select_data
  this.myCircle.classed("selected_second", function(d){return d.properties.name==data})
},
show_period(){
  this.g4.style("display","none")
  let self = this
  var myColor = d3.scaleSequential()
    .domain([0.83,0.42])
    .interpolator(d3Chromatic.interpolatePiYG);
  function choose_color(place){
    var name = place.properties.name
    var res = "rgb(100,149,237)"
    for (var i = 0;i<self.place_color_select.length; i++) {
      var sli = self.place_color_select[i]
      if(name == sli['place']){
        res = myColor(sli['senti'])
      }
    }
    return res
  }

  function choose_id(place){
    var name = place.properties.name
    var res = 5
    for (var i = 0;i<self.place_color_select.length; i++) {
      var sli = self.place_color_select[i]
      if(name == sli['place']){
        var senti = sli['senti']
        if(senti<0.502){
          res = 0
        }
        else if ((senti>0.502)&(senti<0.584)){res = 1}
        else if ((senti>0.584)&(senti<0.666)){res = 2}
        else if ((senti>0.666)&(senti<0.748)){res = 3}
        else if ((senti>0.748)){res = 4}
      }
    }
    return res
  }
  this.myCircle.attr("fill", function(d){return choose_color(d)})
  this.myCircle.attr("opacity",function(d){
    var id = choose_id(d)
    if(self.hover_period==6){
       return 0.7
    }
    if(id==self.hover_period){
      return 1
    }
    else{return 0}
  })
  this.myLink.style("opacity",function(){
    if(self.hover_period==6){ return 0.4}
    else{return 0}
  })},
Get_Predict(predict_all){
  console.log('Map_Get_Predict')
  this.g1_5.selectAll("*").remove()
  for(var i in predict_all){
    var predict = predict_all[i]
    var position = predict['Behavior']
    console.log('position',position)
  if (predict['type']=='Brush'){
    var x_1 = Math.min(Math.max(0,position['x_position1']),500)
    var y_1 = Math.min(Math.max(0,position['y_position1']),650)
    var x_2 = Math.min(Math.max(x_1+20,position['x_position2']),500)
    var y_2 = Math.min(Math.max(y_1+20,position['y_position2']),650)

    this.g1_5.append('rect')
  .attr('x', x_1)
  .attr('y', y_1)
  .attr('width', x_2-x_1)
  .attr('height', y_2-y_1)
  .attr('stroke', 'black')
  .attr('stroke-width',"1px")
  .attr("opacity",0.5)
  .attr('fill', '#69a3b2');

      this.g1_5.append('text')
  .attr('x', x_1)
  .attr('y', y_1)
  .text('Brush')
  .attr('stroke', 'black')
  .attr('stroke-width',"1px")
  .style("font-size","14px");
  }
  
  if (predict['type']=='Zoom'){
    var scale = position['scale']
    var delta_x = position['delta_x']
    var delta_y = position['delta_y']
    var width_rec = 500/scale
    var height_rec = 640/scale
    var x1 = Math.max(0,-delta_x)
    var y1 = Math.max(0,-delta_y)
        this.g1_5.append('rect')
  .attr('x', x1)
  .attr('y', y1)
  .attr('width', width_rec)
  .attr('height', height_rec)
  .attr('stroke', 'black')
  .attr('stroke-width',"1px")
  .attr("opacity",0.1)
  .attr('fill', '#69a3b2');

      this.g1_5.append('text')
  .attr('x', x1)
  .attr('y', y1)
  .text('Zoom')
  .attr('stroke', 'black')
  .attr('stroke-width',"2px")
  .style("font-size","14px");
  }
  
  if (predict['type']=='Click'){
    if(predict['Object_View']=='Map'){
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
  .attr('r', 7)
  .attr('stroke', 'black')
  .attr("stroke-width",'4px')
  .attr("opacity",1)
  .attr('fill', '#69a3b2');}}
  }


}

}}
</script>
<style>

.selected_first {
  stroke: black;
  stroke-width: 1px;
}
.selected_second {
  opacity: 1;
  stroke: black;
  stroke-width: 3px;
  fill: orange;
  r:6px;
}
.subunit.SCT { fill: #ddc; }
.subunit.WLS { fill: #cdd; }
.subunit.NIR { fill: #cdc; }
.subunit.ENG { fill: #dcd; }

.subunit.IRL,
.subunit-label.IRL {
  display: none;
}

.subunit-boundary {
  fill: none;
  stroke: #777;
  stroke-dasharray: 2,2;
  stroke-linejoin: round;
}

.subunit-boundary.IRL {
  stroke: #aaa;
}

.subunit-label {
  fill: #777;
  fill-opacity: .5;
  font-size: 20px;
  font-weight: 300;
  text-anchor: middle;
}
.place-point
.place
.place-label {
  fill: #444;
}

text {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 10px;
  pointer-events: none;
}
#label {
  position: absolute;
  left: 10px;
  font-weight: 100;
  font-family: "Proxima Nova", "Montserrat", sans-serif;
}

.hover {
    fill: yellow;   
}
.desplegable {
        left: 10px;
        top: 5px;
    }
/*
#sliderContainer {
    text-align: center;
    top: 600px;
    left:10px;
}
#histplot{
    text-align: center;
    top: 600px;
    left:10px;
}
#map {
    top: 2000px;
    left:1000px;
}
*/
</style>