

    // Warming Stripes

    // variables
    var w = 300;
    var h = 20;
    var barPadding = 2;
    var color = '#008fd5';
    var min = d3.min(data);
    var max = d3.max(data);

    // YScale
    var yScale = d3.scaleLinear().domain([0, max]).range([0, h]);

    // Color & Opacity scales
    var colorFill = d3.scaleLinear().domain([0,max]).range(["#fefefe", color]);
    var colorOpacity = d3.scaleLinear().domain([0,max]).range([.3, 1]);

    // d3 chart
    d3.select("div#svgTimeline")
        .append("svg")
        .attr('width', w)
        .attr('height', h)
        .selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('width', w / data.length - barPadding)
        .attr('height', h)
        .attr('x', function(d, i){ return i * (w / data.length);})
        .attr('fill', colorFill)
        .style('opacity', colorOpacity)  

    // end of chart


    // Bar chart

    // Data variables
    var phase = {{ phase | safe }};

    var data = Object.values(phase.nct_id);
    var keys = Object.values(phase.phase);  
    console.log(data, keys);

    // variables
    var w = 790;
    var h = 200;
    var barPadding = 1;
    var color = '#008fd5';
    var min = d3.min(data);
    var max = d3.max(data);

    // chart
    var yScale = d3.scaleLinear().domain([0, max]).range([0, h]);


    d3.select("div#phase")
        .append("svg")
        .attr('width', w)
        .attr('height', h)
        .style('padding', '5px')
        .selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('width', w / data.length - barPadding)
        .attr('height', function(d) {return yScale(d);})
        .attr('x', function(d, i){ return i * (w / data.length);})
        .attr('y', function (d) {return h - yScale(d);})
        .attr('fill', color)
        .style('opacity', 0.8)
        

    // end of chart

