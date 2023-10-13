import * as d3 from "d3";



function draw(svg, src, type, width, height) {
  let scale = d3.scaleLinear();
  scale.domain(lib[type]['scale']['domain'](src,width,height));
  scale.range(lib[type]['scale']['range'](src,width,height));

  //https://ghenshaw-work.medium.com/customizing-axes-in-d3-js-99d58863738b
  let xAxisGenerator = d3.axisBottom(d3.scaleLinear().domain([0,12]).range([0,width]))
  //xAxisGenerator.ticks(3);
  //xAxisGenerator.tickValues([3,5,9]);
  //xAxisGenerator.tickFormat(d3.format(".5s"));
  let tickLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  xAxisGenerator.tickFormat((d,i) => tickLabels[i]);
  xAxisGenerator.tickSize(-200);
  let xAxis = d3.select(svg).append('g').call(xAxisGenerator);
  xAxis.attr("transform",`translate(${50},${height*0.91})`);

  let yAxisGenerator = d3.axisLeft(d3.scaleLinear().domain([0,height*0.91]).range([height*0.91,0]))
  let yAxis = d3.select(svg).append('g').call(yAxisGenerator);
  yAxis.attr("transform",`translate(${40},${0})`);

  


  let group = d3.select(svg).append('g').attr("transform",`translate(${40},${0})`);

  src.forEach((d,i,g) => {
    let element = group.append(lib[type]['elem'])

    for(let attr of Object.keys(lib[type]['attr'])){
      element.attr(attr, lib[type]['attr'][attr](d,i,g,scale,width, height))
    }

    for(let style of Object.keys(lib[type]['style'])){
      element.style(style, lib[type]['style'][style]())
    }
  });
}



const lib = {
  T1:{
    scale:{
      domain: (src,width,height)=>[0,getMax(src)],
      range: (src,width,height)=>[0, height * 0.9]
    },
    elem:'rect',
    attr:{
      x:(d,i,g,scale,width, height)=>i*50,
      y:(d,i,g,scale,width, height)=>height * 0.91 - scale(Object.values(d)),
      width:(d,i,g,scale,width, height)=>"40",
      height:(d,i,g,scale,width, height)=>scale(Object.values(d))
    },
    style:{
      fill:()=>'black'
    },
  },
  T2:{
    scale:{
      domain: (src,width,height)=>[0,getMax(src)],
      range: (src,width,height)=>[0, height * 0.9]
    },
    elem:'path',
    attr:{
      d:(d,i,g,scale,width, height)=>pathPoints(d, i, g, scale, height)
    },
    style:{
      stroke:()=>'red',
      'stroke-width':()=>2,
    },
  },
}




function getMax(arr) {
  let max = 0;
  for (let item of arr) {
    if (Number(Object.values(item)) > max) {
      max = Number(Object.values(item));
    }
  }
  return max;
}


function pathPoints(d, i, g, scale, height){
  var path = d3.path();
  let x; let y;
  if (i==0){ x = 0; y = height * 0.91;
  } else { x = (i-1)*50; y = height * 0.91 - scale(Number(Object.values(g[i-1]))) }
  path.moveTo(x, y);
  x = i * 50;
  y = height * 0.91 - scale(Number(Object.values(d)))
  path.lineTo(x, y);
  return path
}






export { draw };
