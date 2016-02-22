$( document ).ready(function() {
    update_triggers();

    $("select.related_to").prepend("<option disabled value='0' selected='selected'>Select an option</option>");

    $("select.related_to").each(function (d) {
        var default_value = parseInt($(this).attr("default"));
        $(this).children("option").each(function (d) {
            if(parseInt($(this).attr("value")) === default_value){
                $(this).parent().val(default_value);
            }
        });

        update_legends($(this));
    });

    //Collapse existing relationship sections
    $(".collapse.relationship-section").each(function (d) {
        if($(this).children('div.btn-success').length > 0){
            console.log('Show it')
        }
        else {
            console.log('hide it');
        }

       if($(this).attr("id") != "collapse-0") {
           $(this).collapse();
       }
    });
});

function update_triggers() {
    //Change related to label when selecting a new relationship
    $('.related_to').change(function() {
        update_legends($(this));
    });

    //Change related to label when changing name
    $('#name').change(function () {
        $('.sub-legend').each(function () {
            var current_id = $(this).attr('id').match(/\d+/)[0];

            var related_to_input = $('#relationships-' + current_id +'-related_to');

            update_legends(related_to_input);
        });
    });

    //Toggle visibility of the bidirectional form
    $('input.bidirectional').change(function () {
        var the_id = $(this).attr('id').match(/\d+/)[0];
        $('#bidirectional-' + the_id).collapse('toggle');
    });
}

function possesive_name(name) {
    name = $.trim(name)

    if(name.match(/[sS]$/)) {
        return name + "'";
    }
    else {
        return name + "'s";
    }
}

function update_legends(related_to_input) {
    var current_id = related_to_input.attr('id').match(/\d+/)[0];

    if($('#name').val() === "" || related_to_input.children('option:selected').text() == 'Select an option'){
        $('#sublegend-' + current_id).html("New Relationship");
        $('#bidirectional-legend-' + current_id).text("Bidirectional Relationship");
    }

    else{
        $('#sublegend-' + current_id).html(possesive_name($('#name').val())
        + ' relationship with '
        + related_to_input.children('option:selected').text());

    $('#bidirectional-legend-' + current_id).text(possesive_name(related_to_input.children('option:selected').text())
        + " relationship with "
        + $('#name').val());
    }
}
