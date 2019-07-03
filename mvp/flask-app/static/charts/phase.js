// BAR CHART (PHASES)

    // Chart variables
    const marginBar = 20;
    const wBar = 960;
    const hBar = 200 - marginBar;

    var wFullHeight = hBar + marginTimeline;

    // Scales
    const yScaleBar = d3.scaleLinear().domain([0, phaseMax]).range([0, wFullHeight]);
    // const xScaleBar = d3.scaleLinear().domain([0, phaseData.length]).range([0, wBar]);
    const xScaleBar = d3.scaleBand().domain(phaseKeys).range([0, wBar], 10, 10);

    const colorFillBar = d3.scaleLinear().domain([0, phaseMax]).range([colorPalette[0], colorPalette[1]]);

    // Main svg
    var svgPhase = d3.select("div#phase")
        .append("svg")
        .attr('width', wBar)
        .attr('height', wFullHeight)
        .call(responsiveChart);

    // xAxis
    var xAxisBar = d3.axisBottom()
                  .scale(xScaleBar);

    svgPhase.append('g')
            .attr("class", "x axis")
            .attr("transform", "translate(0," + hBar + ")")
            .call(xAxisBar);

    var rectPhases = svgPhase.selectAll('rect')
                      .data(phaseData)
                      .enter()
                      .append('rect');

    var attrPhases =  rectPhases.attr('width', wBar / phaseData.length - barPadding)
                                .attr('height', function(d) {return yScaleBar(d);})
                                .attr('x', function(i, d){ return d * (wBar / phaseData.length);})
                                .attr('y', function (d) {return hBar - yScaleBar(d);})
                                .attr('fill', function(d) {return colorFillBar(d);})
                                .on("mouseover", function(i, d) {    
                                      div.transition()    
                                          .duration(200)    
                                          .style("opacity", .9);    
                                      div .html(i + "<br/>"  + phaseKeys[d])  
                                          .style("left", (d3.event.pageX) + "px")   
                                          .style("top", (d3.event.pageY - 40) + "px")  
                                      })          
                                .on("mouseout", function(d) {   
                                    div.transition()    
                                        .duration(500)    
                                        .style("opacity", 0); 
                                  });
                                

    // end of chart

