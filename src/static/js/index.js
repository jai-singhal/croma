function backupAjax(forcefully) {
    $.ajax({
        type: 'GET',
        url: '/ajax/backup',
        data: {
            "forcefully": forcefully
        },
        beforeSend: function () {
            $(".loading").show();
        },
        success: function (response) {
            alert("Backup stored successfully!!")
        },
        error: function (response) {
            var statusCode = response["responseJSON"]["code"]
            if (statusCode === 202) {
                var r = confirm(response["responseJSON"]["message"]);
                if (r == true) {
                    $(".loading").show();
                    backupAjax(1);
                }
            } else if (statusCode === 201 || statusCode === 203) {
                alert(response["responseJSON"]["message"]);
            } else {
                alert("Something went wrong!!")
            }
        },
        complete: function () {
            $(".loading").hide();
        },
    });
}

$(".home").addClass("active");
LoadAutoCompleteItemData();
$(document).unbind("keyup").keyup(function (e) {
    if (e.which == 118) {
        $("#search_item_modal").modal("toggle");
    }
});
$("#id_backup").click(function () {
    var r = confirm("Do you want to take update of Database for today?");
    if (r == true) {
        backupAjax(0);
    }
});