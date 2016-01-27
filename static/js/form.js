$( document ).ready(function() {
    //Change related to label when selecting a new relationship
    $('.related_to').change(function() {
        $(this).closest('fieldset').find('legend').html('Relationship with ' + $(this).children('option:selected').text())
    });

    //When switching to a bidirectional relationship, show the rest of the form
    $('input.bidirectional').checkboxpicker().change(function() {
        console.log("HI!");
        if($(this).prop('checked') === true){
            $(this).parent().parent().child()
            $(this).closest('div.bidirectional').removeClass('hidden');
        }
        else if($(this).prop('checked') === false){
            $(this).closest('div.bidirectional').removeClass('hidden');
        }

    });

    //Activate checkbox JS
    $(':checkbox').checkboxpicker();
});
