var devtracker = {
    crud : {
        del : function(obj) {
            document.del_form.action += "/delete/" + obj.val();
            document.del_form.submit();
        }
    }
}

$(document).ready(function() {
    $(".crudTable .del").click(function() {
        if(confirm("Are you sure you want to delete this?")) {
            devtracker.crud.del($(this));
        } else {
            $(".crudTable .del").attr("checked", false);
        }
    });

    $(".crudTable .dataRow").click(function() {
       var obj = $(this).parent();
       var href = obj.attr("href");
       obj.css("background-color", "#B5D5FF");
       top.location = href;
    });

    $("#crudNew").click(function() {
        top.location = (top.location+"").replace("all", "") + "new";
    });

    $("#cancelEdit").click(function() {
        top.location = $(this).attr("path");
    });

    $("#viewAll").click(function() {
       top.location = top.location + "all";
    });

    $("#viewRecent").click(function() {
        top.location = (top.location+"").replace("all", "");
    });

    $("#edit, .crudTable").fadeIn("fast");

    //Check to see if any content is in the message
    if($("#message").html() != "") {
        $("#message").slideDown("fast", function() {
            var obj = $(this);
            setTimeout(function() {
                obj.slideUp("fast");
            }, 2000);
        });
    }

    $("#exportButton").click(function() {
        var obj = $(this);
        window.open (obj.attr("href"), "Export");
    });

    //If we are on a detail page then select the first input of the form
    if($("#crud_form").length > 0) {
        //console.log($("#crud_form").children();
        var idx=0;
        $('#crud_form p input[readonly!="readonly"]:first').focus();
    }

    $(".datePicker").datepicker();
});