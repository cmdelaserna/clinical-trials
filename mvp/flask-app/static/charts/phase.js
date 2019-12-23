
// BAR CHART (PHASES)

    // Data
    const phaseMax = d3.max(d3.values(phase['All Trials']));
    const phaseKeys = d3.keys(phase['All Trials']); 
    const phaseData = d3.values(phase['All Trials']);

    const phaseDataRecruiting = d3.values(phase['Recruiting']);
    const phaseRecruitingMax = d3.max(d3.values(phase['Recruiting'])); 

    // Chart dimensions and margins
    let marginBar = 20;
    let wBar = 960;
    let hBar = 200 - marginBar;
    let wFullHeight = hBar + marginTimeline;


    // Scales
    const yScaleBar = d3.scaleLinear().domain([0, phaseMax]).range([0, wFullHeight]);
    // const xScaleBar = d3.scaleLinear().domain([0, phaseData.length]).range([0, wBar]);
    const xScaleBar = d3.scaleBand().domain(phaseKeys).range([0, wBar], 10, 10);

    const colorFillBar = d3.scaleLinear().domain([0, phaseMax]).range([colorPalette[0], colorPalette[1]]);
    const colorBarRecruiting = d3.scaleLinear().domain([0, phaseRecruitingMax]).range([colorPalette[0], colorPalette[1]]);

    //
    // Main svg - phase chart
    //
    let svgPhase = d3.select("div#phase")
        .append("svg")
        .attr('width', wBar)
        .attr('height', wFullHeight)
        .call(responsiveChart);

    // Initialize xAxis
    let xAxisBar = d3.axisBottom()
                  .scale(xScaleBar);

    svgPhase.append('g')
            .attr("class", "x axis")
            .attr("transform", "translate(0," + hBar + ")")
            .call(xAxisBar);

    function phaseChart(intialData, colorPhase) {
      let rectPhases = svgPhase.selectAll('rect')
                        .data(intialData)
                        .enter()
                        .append('rect');

      let attrPhases =  rectPhases.attr('width', wBar / intialData.length - barPadding)
                                  .attr('height', function(d) {return yScaleBar(d);})
                                  .attr('x', function(i, d){ return d * (wBar / intialData.length);})
                                  .attr('y', function (d) {return hBar - yScaleBar(d);})
                                  .attr('fill', function(d) {return colorPhase(d);})
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

      attrPhases.exit().remove();
      // End chart function
    }

    phaseChart(phaseData, colorFillBar);

    //radio button
    radioButtons.on('change', function(d) {
        d3.selectAll("rect").remove();
        let newData = this.value

        if (newData == 'timelineData') {
            updateData(timelineData, colorFillTimeline);
            phaseChart(phaseData, colorFillBar);

            // console.log(newData);
        } else {
            updateData(timelineRecruiting, colorTimelineRecruiting);
            phaseChart(phaseDataRecruiting, colorBarRecruiting);
            // console.log(newData);
        }       

    });


