function show_json() {
    $.getJSON('/graph-query.json', function (data) {
        var items = [];

        $.each(data.results.nodes, function (key, val) {
            items.push("<li>" + key + ": " + val.id + "</li>");
        });

        $("<ul/>", {
            "class": "data-items",
            html: items.join("")
        }).appendTo("#graph");
    });
}

function show_graph() {
    var width = 960,
        height = 500;

    var svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .gravity(.05)
        .distance(100)
        .charge(-100)
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
            .attr("r", "5")

        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name
            });

        force.on("tick", function () {
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

            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        })
    });
}

function update_graph() {
    d3.json('/graph-query.json', function (data) {
        d3.select("#graph")
            .append()
    });
}

$(function () {

    //show_json();
});