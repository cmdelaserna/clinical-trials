// BAR CHART (PHASES)

    // Chart variables
    const wBar = 400;
    const hBar = 200;
    const marginBottom = 50;

    // Scales
    const yScaleBar = d3.scaleLinear().domain([0, phaseMax]).range([0, hBar]);

    var colorFillBar = d3.scaleLinear().domain([0, phaseMax]).range([colorPalette[0], colorPalette[1]]);

    // X Axes
    
    var svgPhase = d3.select("div#phase")
        .append("svg")
        .attr('width', wBar)
        .attr('height', hBar + marginBottom);


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

