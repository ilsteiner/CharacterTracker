(function () {
    $('select').prepend("<option disabled value='0' selected='selected'>Select an option</option>");
}).call(this);

$(function () {
    if ($('search-characters')) {
        var search_form = $('#name, #description_snippet')

        search_form.on('input', function () {
            submit_search(function (names) {
                update_list(names);
            });
        });
    }
});

function submit_search(names) {
    if ($('#name').val().length > 0 || $('#description_snippet').val().length > 0) {
        var data = {};
        data["name"] = $('#name').val()
        data["description_snippet"] = $('#description_snippet').val();
        var json_data = JSON.stringify(data);

        $.ajax({
            type: 'POST',
            url: '/search-characters',
            data: json_data,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: names,
            error: function (msg) {
                console.log(msg);
                console.log(json_data);
            }
        });
    }
}

function update_list(names) {
    var name_list_1 = $('#name-list-1');

    var name_list_2 = $('#name-list-2');

    name_list_1.empty();

    name_list_2.empty();

    var counter = 0;

    $.each(names, function (index, items) {
        $.each(items, function (index, item) {
            if (typeof item.name != "undefined") {
                counter++;
                if(counter <= 5){
                    name_list_1.append('<li>' + item.name + '</li>');
                }
                else if(counter <= 9){
                    name_list_2.append('<li>' + item.name + '</li>');
                }
                else if(counter == 10){
                    name_list_2.append('<li>...</li>');
                }
            }
        });
    });

    update_graph(names)
}