import ChartRender from './chart-render.js';

export default class ChartRenderTaxonomyOverlap extends ChartRender{
    constructor(url=null, analysisPk=null){
        super(url, analysisPk);
        this.elementIdRoot = "taxonomy-overlap-chart";
    }
    formatDataChart(){
    }
    renderChart(){
        // create the svg area
        const svg = d3.select("#taxonomy-overlap-chart").append("svg")
            .attr("width", 500).attr("height", 500).append("g").attr("transform", "translate(250,250)")
        // create a matrix
        const matrix = this.data;
        const names = this.labels;

        // give this matrix to d3.chord(): it parses for rendering arcs and ribbons
        const res = d3.chord().padAngle(0.1).sortSubgroups(d3.descending)(matrix)
        // add the groups on the inner part of the circle
        svg.datum(res).append("g").selectAll("g").data(function(d) { return d.groups; })
        .enter().append("g").append("path")
        .style("fill", "grey").style("stroke", "black")
        .attr("d", d3.arc()
          .innerRadius(170)
          .outerRadius(180)
        )

        // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
        // Its opacity is set to 0: we don't see it by default.
        const tooltip = d3.select("#taxonomy-overlap-chart").append("div")
            .style("opacity", 0).attr("class", "tooltip")
            .style("background-color", "white").style("border", "solid")
            .style("border-width", "1px").style("border-radius", "5px")
            .style("padding", "10px")

        // A function that change this tooltip when the user hover a point.
        // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
        const showTooltip = function(d) {
            tooltip.style("opacity", 1)
                .html(names[d.source.index] + " - " + names[d.target.index])
                .style("left", (d3.event.pageX + 15) + "px")
                .style("top", (d3.event.pageY - 28) + "px")
        }

        // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
        const hideTooltip = function(d) {
            tooltip.transition().duration(50).style("opacity", 0)
        }
        // Add the links between groups
        svg.datum(res).append("g").selectAll("path").data(function(d) { return d; })
            .enter().append("path").attr("d", d3.ribbon().radius(160))
            .style("fill", "#69b3a2").style("stroke", "black")
            .on("mouseover", showTooltip).on("mouseleave", hideTooltip)
       }
}
