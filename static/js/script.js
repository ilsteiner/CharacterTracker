(function() {
    $('select').prepend("<option disabled value='0' selected='selected'>Select an option</option>");
}).call(this);

$( document ).ready(function() {
    $('.related_to').change(function() {
        $(this).closest('fieldset').find('legend').html('Relationship with ' + $(this).children('option:selected').text())
    })
});
