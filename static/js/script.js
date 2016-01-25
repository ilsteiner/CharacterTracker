(function() {
    $('select').prepend("<option disabled value='0' selected='selected'>Select an option</option>");
}).call(this);

$( document ).ready(function() {
    //Change related to label when selecting a new relationship
    $('.related_to').change(function() {
        $(this).closest('fieldset').find('legend').html('Relationship with ' + $(this).children('option:selected').text())
    })

    //Activate checkbox JS
    $(':checkbox').checkboxpicker();
});


