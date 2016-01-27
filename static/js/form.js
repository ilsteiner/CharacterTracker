$( document ).ready(function() {
    //Change related to label when selecting a new relationship
    $('.related_to').change(function() {
        $(this).closest('fieldset').find('legend').html('Relationship with ' + $(this).children('option:selected').text())
    })

    //Activate checkbox JS
    $(':checkbox').checkboxpicker();
});
