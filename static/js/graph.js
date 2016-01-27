function show_graph() {
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

$(function () {
    show_graph();
});