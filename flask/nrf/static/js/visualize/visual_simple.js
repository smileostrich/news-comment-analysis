var WIDTH = 300;
var HEIGHT = 400;

var TOP_MARGIN = 10;
var LEFT_MARGIN = 30;
var RIGHT_MARGIN = 10;
var BOTTOM_MARGIN = 10;

var scores = [];
var comment = {{ comment }}
var news = {{ news }}
// scores.push({{ comment }}, {{ news }});
scores.push(comment, news);

var yScale = d3.scaleLinear()
    .domain([0, d3.max(scores)])
    .range([HEIGHT - TOP_MARGIN - BOTTOM_MARGIN, 0]);
var xScale = d3.scaleBand()
    .domain(d3.range(scores.length))
    .range([0, WIDTH - LEFT_MARGIN - RIGHT_MARGIN])
    .padding(0.1);

var root = d3.select('svg')
    .attr('width', WIDTH)
    .attr('height', HEIGHT);

root.select('.y-axis')
    .style('transform', 'translate(' + LEFT_MARGIN + 'px, ' + TOP_MARGIN + 'px)')
    .call(d3.axisLeft().scale(yScale));

root.select('.bars')
    .style('transform', 'translate(' + LEFT_MARGIN + 'px, ' + TOP_MARGIN + 'px)')
    .selectAll('rect')
    .data(scores)
    .attr('x', function (score, index) {return xScale(index);})
    .attr('y', function (score, index) {return yScale(score);})
    .attr('width', xScale.bandwidth())
    .attr('height', function (score, index) {
        return HEIGHT - TOP_MARGIN - BOTTOM_MARGIN - yScale(score);
    });