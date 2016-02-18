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

function update_graph(filter) {
    $('svg').remove();
    show_graph(filter);
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

function size_graph() {
    var graph = $('#graph');

    graph.attr("width", get_width());

    graph.attr("height", get_height());
}

//Taken from: http://bl.ocks.org/mbostock/3750558
function show_graph() {
    var width = 960,
        height = 500;

    var force = d3.layout.force()
        .size([width, height])
        .charge(-400)
        .linkDistance(40)
        .on("tick", tick);

    var drag = force.drag()
        .on("dragstart", dragstart)
        .on("dragend", dragend);

    var svg = d3.select("#graph_container").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("id", "graph");

    size_graph();

    width = get_width();

    height = get_height();

    var link = svg.selectAll(".link"),
        node = svg.selectAll(".node");

    d3.json("/graph-query.json", function (error, graph) {
        if (error) throw error;

        force
            .nodes(graph.results.nodes)
            .links(graph.results.links)
            .start();

        link = link.data(graph.results.links)
            .enter().append("line")
            .attr("class", "link");

        node = node.data(graph.results.nodes)
            .enter().append("g")
            .attr("class", "node")
            .append("circle")
            .attr("r", 12)
            .on("dblclick", dblclick)
            .call(drag);

        node.append("svg:title")
         .each(function (d) {
         d3.select(this).text(d.name);
         });
    });

    function tick() {
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

        node.attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });

        node.select("text").attr("dx", function (d) {
            console.log(d.element("circle").attr("cx"));
           return d.element("circle").attr("cx");
        }).attr("dy", function (d) {
           return d.element("circle").attr("cy");
        });
    }

    function dblclick(d) {
        d3.select(this).classed("fixed", d.fixed = false);
        d3.select(this.parentNode).select("text").remove();
    }

    function dragstart(d) {
        d3.select(this).classed("fixed", d.fixed = true);
        d3.select(this.parentNode).select("text").remove();
        d3.select(this).select("title").text(d.name);
    }

    function dragend(d) {
        d3.select(this.parentNode)
            .append("text")
            .text(d.name)
            .attr("dx", d3.select(this).attr("cx"))
            .attr("dy", d3.select(this).attr("cy"))
            .attr("text-anchor", "middle");

        d3.select(this.parentNode)
            .select("text")
            .attr("y", d3.select(this.parentNode).attr("y") + 20)
            .append("svg:title")
            .text(d.short_description);

        d3.select(this).select("title").text(d.short_description);
    }
}

$(function () {
    show_graph();

    $(window).on("resize", size_graph());
});