
// Responsive function

function responsiveChart(svg) {
    // get container + svg aspect ratio
    var container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style("width")),
        height = parseInt(svg.style("height")),
        aspect = width / height;

    // add viewBox and preserveAspectRatio properties,
    // and call resize so that svg resizes on inital page load
    svg.attr("viewBox", "0 0 " + width + " " + height)
        .attr("perserveAspectRatio", "xMinYMid")
        .call(resize);

    // to register multiple listeners for same event type, 
    // you need to add namespace, i.e., 'click.foo'
    // necessary if you call invoke this function for multiple svgs
    // api docs: https://github.com/mbostock/d3/wiki/Selections#on
    d3.select(window).on("resize." + container.attr("id"), resize);

    // get width of container and resize svg to fit it
    function resize() {
        var targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect));
    }
}



// CHART: TIMELINE

    // Chart variables
    const marginTimeline = 30;
    const height = 50 - marginTimeline;

    const wTimeline = 960;
    const hTimeline = height + marginTimeline;
    const barPadding = 1;

    // Color Palette
    // https://gka.github.io/palettes/#/9|s|00429d,96ffea,ffffe0|ffffe0,ff005e,93003a|1|1
    
    const colorPalette = ['#70ccf6', '#00a6ff']; // blue
    const gray = '#f1f1f1';
    const color = colorPalette[1];

    // Scales
    const yScaleTimeline = d3.scaleLinear().domain([0, timelineMax]).range([0, hTimeline]);
    const xScaletimeline = d3.scaleBand().domain(timelineDataYear).range([0, wTimeline], 5, 5);
    
    const colorFillTimeline = d3.scaleLinear().domain([0, timelineMax]).range([colorPalette[0], colorPalette[1]]);

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
                        .attr('height', hTimeline)
                        .call(responsiveChart);

     // xAxis
    var xAxisTimeline = d3.axisBottom()
                        .scale(xScaletimeline);

    svgTimeline.append('g')
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxisTimeline);


    var rectTimeline = svgTimeline.selectAll('rect')
                        .data(timelineData)
                        .enter()
                        .append('rect');

    var attrTimeline = rectTimeline
                        .attr('width', wTimeline / timelineData.length - barPadding)
                        .attr('height', height)
                        // .attr('height', function(d) {return yScaleTimeline(d);})
                        .attr('x', function(d, i){ return i * (wTimeline / timelineData.length);})
                        // .attr('y', hTimeline)
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
                            div .html(i + " entries "  + " in " + timelineDataYear[d])  
                                .style("left", (d3.event.pageX) - 10 + "px")   
                                .style("top", (d3.event.pageY - 40) + "px")  
                            })          
                        .on("mouseout", function(d) {   
                            div.transition()    
                                .duration(500)    
                                .style("opacity", 0); 
                        });
    
    // end of chart