//The jQuery Setup
$(document).ready(function () {

    $('#insert-new').click(function () {
        var yourclass = ".relationship";  //The class you have used in your form
        var clonecount = $(yourclass).length;	//how many clones do we already have?
        var newid = Number(clonecount);		//Id of the new clone, we're zero indexed so don't add 1

        $(yourclass + ":last").fieldclone({		//Clone the last element
            newid_: newid,						//Id of the new clone, (you can pass your own if you want)
            target_: $("#insert-new"),			//where do we insert the clone? (target element)
            insert_: "after",					//where do we insert the clone? (after/before/append/prepend...)
            limit_: 10							//Maximum Number of Clones
        });

        //Update any triggers on relationship section items
        update_triggers();

        return false;
    });
});

//The Plugin Script
(function ($) {

    $.fn.fieldclone = function (options) {

        //==> Options <==//
        var settings = {
            newid_: options.newid_,
            target_: $(this),
            insert_: options.insert_,
            limit_: options.limit_
        };
        if (options) $.extend(settings, options);

        if ((settings.newid_ <= (settings.limit_ + 1)) || (settings.limit_ == 0)) {	//Check the limit to see if we can clone

            //==> Clone <==//
            var fieldclone = $(this).clone();
            var node = $(this)[0].nodeName;
            var classes = $(this).attr("class");

            /*
             * This is where the name and ID are incremented. I had to rewrite it for my use case.
             * */
            $(fieldclone).find(':input,div.bidirectional').each(function () {
                var oldname = $(this).attr("name");
                var oldid = $(this).attr("id");
                if(oldname){
                    console.log('Name: ' + oldname + ' > ' + oldname.replace(/-\d-/, '-' + options.newid_ + '-'));
                    $(this).attr("name", oldname.replace(/-\d/, '-' + options.newid_));
                }
                if(oldid){
                    console.log('ID: ' + oldid + ' > ' + oldid.replace(/-\d-/, '-' + options.newid_ + '-'));
                    $(this).attr("id", oldid.replace(/-\d/, '-' + options.newid_));
                }
            });

            //Fix the legend for the fieldset
            $(fieldclone).find('legend').html('New Relationship');

            //Fix the collapse link
            $(fieldclone).find('a').attr('href','#collapse-'+options.newid_);

            //Fix the collapse div
            $(fieldclone).find('.relationship-section.collapse').attr('id','collapse-'+options.newid_);

            //==> Locate Target Id <==//
            var targetid = $(settings.target_).attr("id");
            if (targetid.length <= 0) {
                targetid = "clonetarget";
                $(settings.target_).attr("id", targetid);
            }

            //Collapse existing rows
            //$('.relationship .collapse').removeClass('in').each($(this).collapse());

            //==> Insert Clone <==//
            var newhtml = $(fieldclone).html().replace(/\n/gi, "");
            newhtml = '<' + node + ' class="' + classes + '">' + newhtml + '</' + node + '>';

            eval("var insertCall = $('#" + targetid + "')." + settings.insert_ + "(newhtml)");
        }
    };

})(jQuery);