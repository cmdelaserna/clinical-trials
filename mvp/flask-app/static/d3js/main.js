// <!-- d3 scripts
//   –––––––––––––––––––––––––––––––––––––––––––––––––– -->

// CHART: TIMELINE

    // Chart variables
    var wTimeline = 350;
    var hTimeline = 15;
    var barPadding = 1;

    // Color Palette
    // https://gka.github.io/palettes/#/9|s|00429d,96ffea,ffffe0|ffffe0,ff005e,93003a|1|1
    
    const colorPalette = ['#00a4f7', '#20458b']; // blue
    const gray = '#f1f1f1';
    const color = colorPalette[1];

    // Scales
    var xScaleTimeline = d3.scaleLinear().range([0, wTimeline]);
    var yScaleTimeline = d3.scaleLinear().domain([0, timelineMax]).range([0, hTimeline]);
    var colorFillTimeline = d3.scaleLinear().domain([0, timelineMax]).range([colorPalette[0], colorPalette[1]]);

    // Div for the tooltip
    var div = d3.select("body")
                .append("div") 
                .attr("class", "tooltip")      
                .style("opacity", 0);

    // Color scales
    // var colorOpacity = d3.scaleLinear().domain([0,maxStripe]).range([.3, 1]);

    // d3 chart
    var svgTimeline = d3.select("div#svgTimeline")
                        .append("svg")
                        .attr('width', wTimeline)
                        .attr('height', hTimeline);

    var rectTimeline = svgTimeline.selectAll('rect')
                        .data(timelineData)
                        .enter()
                        .append('rect');

    var attrTimeline = rectTimeline
                        .attr('width', wTimeline / timelineData.length - barPadding)
                        .attr('height', wTimeline)
                        // .attr('height', function(d) {return yScaleTimeline(d);})
                        .attr('x', function(d, i){ return i * (wTimeline / timelineData.length);})
                        // .attr('y', function (d) {return hTimeline - yScaleTimeline(d);})
                        .attr('fill', function(d) {
                            if (d < 1) {
                                return gray;
                            } else {
                                return colorFillTimeline(d);
                            }
                        })
                        .on("mouseover", function(i, d) {    
                            div.transition()    
                                .duration(200)    
                                .style("opacity", .9);    
                            div .html(d + " entries "  + " in " + timelineDataYear[d])  
                                .style("left", (d3.event.pageX) - 10 + "px")   
                                .style("top", (d3.event.pageY - 40) + "px")  
                            })          
                        .on("mouseout", function(d) {   
                            div.transition()    
                                .duration(500)    
                                .style("opacity", 0); 
                        });
    
    // end of chart

    
    // BAR CHART (PHASES)

    // Chart variables
    var wBar = 600;
    var hBar = 300;
    var barPadding = 1;

    // Scales
    var yScaleBar = d3.scaleLinear().domain([0, maxPhase]).range([0, hBar]);
    var colorFillBar = d3.scaleLinear().domain([0, maxPhase]).range([colorPalette[0], colorPalette[1]]);

    var svgPhase = d3.select("div#phase")
        .append("svg")
        .attr('width', wBar)
        .attr('height', hBar);

    var rectPhases = svgPhase.selectAll('rect')
                      .data(dataPhase)
                      .enter()
                      .append('rect');

    // Phases: Early Phase 1, N/A, Phase 1, Phase 1/Phase 2, Phase 2, Phase 2/Phase 3, Phase 3

    var attrPhases =  rectPhases.attr('width', wBar / dataPhase.length - barPadding)
                                .attr('height', function(d) {return yScaleBar(d);})
                                .attr('x', function(d, i){ return i * (wBar / dataPhase.length);})
                                .attr('y', function (d) {return hBar - yScaleBar(d);})
                                .attr('fill', function(d) {return colorFillBar(d);})
                                .on("mouseover", function(d) {    
                                      div.transition()    
                                          .duration(200)    
                                          .style("opacity", .9);    
                                      div .html(d + "<br/>"  + keysPhase[d])  
                                          .style("left", (d3.event.pageX) + "px")   
                                          .style("top", (d3.event.pageY - 40) + "px")  
                                      })          
                                .on("mouseout", function(d) {   
                                    div.transition()    
                                        .duration(500)    
                                        .style("opacity", 0); 
                                  });

    // end of chart

