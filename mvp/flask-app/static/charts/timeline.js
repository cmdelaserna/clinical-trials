 // D3 barchart - timeline of trials

 // Data variables
    var graphData = {{ timeline_graph | safe }};

    var data = Object.values(graphData.nct_id);
    var keys = Object.values(graphData.year_submitted)

    console.log(data, keys);

    //
    // chart
    //

    // variables
    var w = 400;
    var h = 50;
    var barPadding = 2;
    var color = '#008fd5';
    var min = d3.min(data);
    var max = d3.max(data);


    // chart
    var yScale = d3.scaleLinear().domain([0, max]).range([0, h]);

    // color
    var colorOpacity = d3.scaleLinear().domain([0,max]).range(["#ffffff", color]);

    d3.select("div#svgTimeline")
        .append("svg")
        .attr('width', w)
        .attr('height', h)
        .style('padding', '5px')
        .style('border-bottom', '1px dotted #ddd')
        .selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('width', w / data.length - barPadding)
        .attr('height', function(d) {return yScale(d);})
        .attr('x', function(d, i){ return i * (w / data.length);})
        .attr('y', function (d) {return h - yScale(d);})
        .attr('fill', colorOpacity)
        .style('opacity', 0.8)
        

    // end of chart