$( document ).ready(function() {
    //Change related to label when selecting a new relationship
    $('.related_to').change(function() {
        $(this).closest('fieldset').find('legend').html('Relationship with ' + $(this).children('option:selected').text());
    });

    update_triggers();
});

function update_triggers() {
    console.log('Updating triggers');

    //Toggle visibility of the bidirectional form
    $('input.bidirectional').change(function () {
        var the_id = $(this).attr('id').match(/\d+/)[0];
        $('#bidirectional-' + the_id).collapse('toggle');
    });
}
