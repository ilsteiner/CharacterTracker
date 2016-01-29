function show_json() {
    $.getJSON('/graph-query.json', function (data) {
        var items = [];

        $.each(data.results.nodes, function (key, val) {
            items.push("<li>" + key + ": " + val.id + "</li>");
        });

        $("<ul/>", {
            "class": "data-items",
            html: items.join("")
        }).appendTo("#graph_container");
    });
}

//Largely copied from http://bl.ocks.org/jose187/4733747
function show_graph() {
    var width = 960,
        height = 500,
        radius = 40;

    var svg = d3.select("#graph_container").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("id", "graph");

    size_graph();

    width = get_width();

    height = get_height();

    var force = d3.layout.force()
        .gravity(.05)
        .distance(200)
        .charge(-2000)
        .size([width, height]);

    d3.json('/graph-query.json', function (json) {
        force
            .nodes(json.results.nodes)
            .links(json.results.links)
            .start();

        var link = svg.selectAll(".link")
            .data(json.results.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", function (d) {
                return Math.sqrt(d.weight);
            });

        var node = svg.selectAll(".node")
            .data(json.results.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .attr("r", radius);

        node.append("text")
            .each(function (d) {
                var name_array = d.name.split(" ");
                for (i=0; i < name_array.length; i++){
                    d3.select(this).append("tspan")
                        .text(name_array[i])
                        .attr("text-anchor", "middle")
                        .attr("dy", i ? "1.2em" : 0)
                        .attr("x", 0)
                        .attr("class", "tspan-"+i);
                }
            });

        force.on("tick", function () {

            //Source: http://bl.ocks.org/mbostock/1129492
            node.attr("transform", function (d) {
                var dx = Math.max(radius, Math.min(width - radius, d.x));
                var dy = Math.max(radius, Math.min(height - radius, d.y));
                return "translate(" + dx + "," + dy + ")";
            });

            link.attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            //No bounding box implementation
            /*node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });*/
        })
    });
}

function update_graph() {
    d3.json('/graph-query.json', function (data) {
        d3.select("#graph_contianer")
            .append()
    });
}

function get_width() {
    var graph = $('#graph');

    var container = graph.parent();

    return container.width();
}

function get_height() {
    var graph = $('#graph');
    var aspect = graph.width() / graph.height();
    return Math.round(get_width() / aspect);
}

function size_graph(){
    var graph = $('#graph');

    graph.attr("width", get_width());

    graph.attr("height", get_height());
}

$(function () {
    show_graph();

    size_graph();

    $(window).on("resize", size_graph());
});