var $editMode = false;
var $createMode = false;

function fill_item_table(data) {
    for (var i = 0; i < data.length; i++) {
        var id_name = "batch" + String($uid);
        var edit_id_name = "edit_" + id_name;
        var del_id_name = "del_" + id_name;
        $("#item_batch_table_body").append("<tr id = \'" + id_name + "\'>\
        <td class = 'batch'>" + data[i]['batch_no'] + "</td>\
        <td class = 'expiry'>" + data[i]['expiry'] + "</td>\
        <td class = 'strip'>" + data[i]['strip'] + "</td>\
        <td class = 'nos'>" + data[i]['nos'] + "</td>\
        <td class = 'strip_pur'>" + data[i]['strip_pur'] + "</td>\
        <td class = 'strip_sale'>" + data[i]['strip_sale'] + "</td>\
        <td class = 'mrp'>" + data[i]['mrp'] + "</td>\
        <td class = 'pur_rt'>" + data[i]['pur_rt'] + "</td>\
        <td class = 'sale_rt'>" + data[i]['sale_rt'] + "</td>\
        <td class = 'inst_rt'>" + data[i]['inst_rt'] + "</td>\
        <td class = 'trade_rt'>" + data[i]['trade_rt'] + "</td>\
        <td class = 'buttons'>\
            <button data = \'" + $uid + "\' class = 'edit_row' id = \'" + edit_id_name + "\'>\
                <span class='glyphicon glyphicon-edit' aria-hidden='true'></span></button>\
            <button data = \'" + $uid + "\' class = 'del_row' id = \'" + del_id_name + "\'>\
                <span class='glyphicon glyphicon-trash' aria-hidden='true'></span></button></button>\
        </td></tr>")
        $uid++;
    }
}

function fillEditValues(dataJson) {
    $("#editor")[0].reset()

    $("#editor-modal").modal("toggle");

    $("#batch_no").val(dataJson['batch_no']);
    var expiry = dataJson['expiry'];
    expiry = expiry.slice(5, 7) + "/" + expiry.slice(0, 4);
    $("#expiry").val(expiry);
    $("#strip").val(dataJson['strip']);
    $("#nos").val(dataJson['nos']);
    $("#strip_pur").val(dataJson['strip_pur']);
    $("#strip_sale").val(dataJson['strip_sale']);
    $("#mrp").val(parseFloat(dataJson['mrp']));
    $("#pur_rt").val(parseFloat(dataJson['pur_rt']));
    $("#sale_rt").val(parseFloat(dataJson['sale_rt']));
    $("#inst_rt").val(dataJson['inst_rt']);
    $("#trade_rt").val(dataJson['trade_rt']);
    $("#std_rt").val(dataJson['std_rt']);

}

function HandleEditItem(data) {
    for (var i = 0; i < parseInt($batch_data_set.length); i++) {

        if (data['batch_no'] == $batch_data_set[i]['batch_no'] && $batch_data_set[i]['deleted'] != 1) {
            $batch_data_set[i]['batch_no'] = data['batch_no'];
            $batch_data_set[i]['expiry'] = data['expiry'];
            $batch_data_set[i]['strip'] = data['strip'];
            $batch_data_set[i]['nos'] = data['nos'];

            $batch_data_set[i]['strip_pur'] = data['strip_pur'];
            $batch_data_set[i]['strip_sale'] = data['strip_sale'];
            $batch_data_set[i]['mrp'] = data['mrp'];
            $batch_data_set[i]['pur_rt'] = data['pur_rt'];
            $batch_data_set[i]['sale_rt'] = data['sale_rt'];
            $batch_data_set[i]['inst_rt'] = data['inst_rt'];
            $batch_data_set[i]['trade_rt'] = data['trade_rt'];
            $batch_data_set[i]['inst_rt'] = data['inst_rt'];

            var row_id = "#batch" + String(i);
            $(row_id + " > .expiry").html(data['expiry']);
            $(row_id + " > .strip").html(data['strip']);
            $(row_id + " > .nos").html(data['nos']);
            $(row_id + " > .strip_pur").html(data['strip_pur']);
            $(row_id + " > .strip_sale").html(data['strip_sale']);
            $(row_id + " > .pur_rt").html(data['pur_rt']);
            $(row_id + " > .sale_rt").html(data['sale_rt']);
            $(row_id + " > .inst_rt").html(data['inst_rt']);
            $(row_id + " > .trade_rt").html(data['trade_rt']);
            return false;
        }
    }
    return true;
}

function AddNewRow(data) {
    var id_name = "batch" + String($uid);
    var edit_id_name = "edit_" + id_name;
    var del_id_name = "del_" + id_name;
    $("#item_batch_table_body").append("<tr id = \'" + id_name + "\'>\
        <td class = 'batch'>" + data['batch_no'] + "</td>\
        <td class = 'expiry'>" + data['expiry'] + "</td>\
        <td class = 'strip'>" + data['strip'] + "</td>\
        <td class = 'nos'>" + data['nos'] + "</td>\
        <td class = 'strip_pur'>" + data['strip_pur'] + "</td>\
        <td class = 'strip_sale'>" + data['strip_sale'] + "</td>\
        <td class = 'mrp'>" + data['mrp'] + "</td>\
        <td class = 'pur_rt'>" + data['pur_rt'] + "</td>\
        <td class = 'sale_rt'>" + data['sale_rt'] + "</td>\
        <td class = 'inst_rt'>" + data['inst_rt'] + "</td>\
        <td class = 'trade_rt'>" + data['trade_rt'] + "</td>\
        <td class = 'buttons'>\
            <button data = \'" + $uid + "\' class = 'edit_row' id = \'" + edit_id_name + "\'>\
                <span class='glyphicon glyphicon-edit' aria-hidden='true'></span></button>\
            <button data = \'" + $uid + "\' class = 'del_row' id = \'" + del_id_name + "\'>\
                <span class='glyphicon glyphicon-trash' aria-hidden='true'></span></button></button>\
        </td></tr>")
}

function make_item_search_class() {
    var text = "search_item_";
    var possible = "abcdefghijklmnopqrstuvwxyz";

    for (var i = 0; i < 3; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function keyboard_powered_scroll(total_data, class_name) {
    //handling the batch table
    var tr_id = 0;
    var current_row_selector = $("." + class_name + "0");
    current_row_selector.focus();
    current_row_selector.css("background-color", "#6699FF");

    $(document).keydown(function (e) {
        if (e.keyCode == 13) {
            var selector_class = "." + class_name + tr_id + "a_link";

            var val = $(selector_class).text();
            var url_ = $(selector_class).attr("href");
            window.location = url_;
            $('#search-item').modal('hide');
            return false;
        }
        if (e.keyCode == 38 && tr_id > 0) {
            current_row_selector.css("background-color", "white");
            tr_id -= 1;
            $("#search-res").animate({
                scrollTop: '-=34px'
            }, 1);
            current_row_selector = $("." + class_name + String(tr_id));
            current_row_selector.focus();
            current_row_selector.css("background-color", "#6699FF");

            return false;
        }
        if (e.keyCode == 40 && tr_id < total_data - 1) {
            current_row_selector.css("background-color", "white");
            tr_id += 1;
            $("#search-res").animate({
                scrollTop: '+=34px'
            }, 1);
            current_row_selector = $("." + class_name + String(tr_id));
            current_row_selector.focus();
            current_row_selector.css("background-color", "#6699FF");

            return false;
        }
    });
}


$(document).on('keypress', "input:not([readonly], :disabled, .main-btn, #id_re_qty), select, button", function (e) {
    if (e.which == 13) {
        e.preventDefault();
        var index = $("select:enabled, button, input:not([readonly], :disabled, .main-btn), input[type='search']").index(this) + 1;
        $("select:enabled, button, input:not([readonly], :disabled, .main-btn), input[type='search']").eq(index).focus();
    }
});

$(document).on('keypress', "input:not([readonly], :disabled, .main-btn, #batch_no, #id_name), select", function (e) {
    if (e.shiftKey && e.which == 13) {
        e.preventDefault();
        var index = $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").index(this) - 1;
        $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").eq(index).focus();
    }
});


//SEARCH BUTTON FUNCTIONALITY///////////////////////////////

$("#item-name").focus(function () {
    $("#search-msg").text("");
});
$('#search-item').on('shown.bs.modal', function () {
    $('#item-name').attr("readonly", false);
    $('#item-name').focus();

})
$("#search-btn").focus(function () {
    $(this).click();
})

$("#search-btn").click(function () {
    var item = $('#item-name').val();
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "search_name": item
    };
    $.ajax({
        type: 'GET',
        url: '/item/ajax/search_item',
        data: data,
        beforeSend: function () {
            $(".loading").show();
        },
        complete: function () {
            $(".loading").hide();
        },

        success: function (data) {

            var item_data = data['items_query'];
            var item_data = JSON.parse(item_data);
            var html_text = "<br><br>";
            var total_data = item_data.length;
            var class_name = make_item_search_class();
            if (total_data > 0) {
                $('#item-name').focus();
                $(item_data).each(function (index, element) {
                    var cls_name = class_name + index;
                    var a_class_name = "search_item_url " + cls_name + "a_link";
                    html_text += "<tr class = \'" + cls_name + "\'" + "><td><a class = \'" + a_class_name + "\' href = " + element['url'] + ">" + element['name'] + "</a></td></tr>"
                });
                $("#search-res").html(html_text);
                $("#search-res").css("height", "230px");
                $("#search-res").css("overflow-y", "auto");
                $("#search-res").css("width", "100%");
                keyboard_powered_scroll(total_data, class_name);
            } else {
                $("#search-res").html("<p style = 'font-size:15px; color:red; font-weight:bold; margin-left:15px;'> No Item Found</p>");
                $('#item-name').focus();
            }
        },
        error: function (data) {
            alert(data);
        }
    });

})


$("#expiry").blur(function () {
    expiryValidations();
})

$("#batch_no").blur(function () {
    if ($createMode) {
        var batch = $(this).val();
        for (var i = 0; i < parseInt($batch_data_set.length); i++) {
            if (batch == $batch_data_set[i]['batch_no'] && batch != "" && $batch_data_set[i]['deleted'] != 1) {
                $(this).val("");
                alert("Same batch not allowed");
                $(this).focus();
                return false;
            }
        }
    }
})

$("#batch_add_btn").focus(function () {
    $(this).click();
    $("#editor-modal").modal("toggle");
})

$("#mrp, #pur_rt, #sale_rt, #std_rt").focus(function () {
    var strip_sale = $("#strip_sale").val();
    var strip_pur = $("#strip_pur").val();
    $("#strip_pur").val((strip_pur * 1.0).toFixed(2));
    $("#strip_sale").val((strip_sale * 1.0).toFixed(2));

    $("#mrp").val((strip_sale * 1.0).toFixed(2));
    $("#pur_rt").val((strip_pur * 0.1).toFixed(2));
    $("#sale_rt").val((strip_sale * 0.1).toFixed(2));
    $("#inst_rt").val((strip_sale * 1.0).toFixed(2));
    $("#trade_rt").val((strip_pur * 0.1).toFixed(2));
    $("#std_rt").val((strip_sale - 0.16 * strip_sale).toFixed(2));
});

function getFormData($form) {
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};
    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'].replace(/&amp;/, "&");
    });
    return indexed_array;
}

function saveUpdateItemAjax($this, url) {
    $this.button('loading');
    if ($("#id_name").val() == "") {
        alert("Item name is required")
        $this.button('reset');
        return false;
    }

    localStorage.removeItem("itemData"); // remove the localStorage of itemData JSON data

    var item = getFormData($("#item-form"));
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "batches": $batch_data_set,
        "item": item
    };
    data = JSON.stringify(data);
    $.ajax({
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        url: url,
        datatype: 'json',
        data: data,
        success: function (data) {
            window.location = data.url;
        },
        error: function (data) {
            $this.button('reset');
            if (data.status == 500) {
                alert("Something went wrong!! Contact Jai");
                return false;
            }
            data = data.responseJSON;

            var batch_errors = data['batch_errors'];
            var item_errors = data['item_errors'];
            var batch_error = data['batch_error'];
            $.each(item_errors, function (key, value) {

                $("input[name=" + key + "]").addClass("input_alert");
                alert(key + " = " + value);
            });
            if (batch_errors !== undefined) {
                for (var i = 0; i < batch_errors.length; i++) {
                    var batch_error = batch_errors[i];
                    $.each(batch_error, function (key, value) {
                        alert(key + " = " + value);
                    });
                }
            }
            $.each(batch_error, function (key, value) {
                alert(key + " = " + value);
            });
        },
    });
}

function setInputsDisabled() {
    $("#id_unit_id").prop('readonly', true);
    $("#id_group_id").prop('readonly', true);
    $("#id_salt_id").prop('readonly', true);
    $("#id_godown_id").prop('disabled', true);
    $("#id_stax_id").prop('disabled', true);
    $("#id_ptax_id").prop('disabled', true);
    $("#id_is_active").prop('disabled', true);
    $("#id_is_active").prop('disabled', true);
    $("#id_cgst").prop('disabled', true);
    $("#id_sgst").prop('disabled', true);
}

//Item CODE DISABLED READONLY
$("#id_item_code").prop("disabled", "disabled");

//Batch Modal Configuration
$(".modal-wide").on("show.bs.modal", function () {
    var height = $(window).height() - 200;
    $(this).find(".modal-body").css("max-height", height);
});


function loadAutocomlete() {
    AutoCompleteData("/company/api/chain-list/?format=json", 'companyData', "#id_group_id", 25, 1);
    AutoCompleteData("/salt/api/list/?format=json", 'saltData', "#id_salt_id", 25, 1);
    AutoCompleteData("/unit/api/list/?format=json", "unitData", "#id_unit_id", 25, 1);
}

$(document).ready(function () {
    $('form:first *:input[type!=hidden]:first').focus();
    $("#add_unit").click(function () {
        localStorage.removeItem("unitData"); // remove the localStorage of unitData JSON data
    })
    $("#add_company, #edit_company").click(function () {
        localStorage.removeItem("companyData"); // remove the localStorage of companyData JSON data
    })
    $("#add_salt, #edit_salt").click(function () {
        localStorage.removeItem("saltData"); // remove the localStorage of saltData JSON data
    })
    $("input").focus(function () {
        $(this).removeClass("input_alert");
    })

    $(".item_master").addClass("active");

    LoadAutoCompleteItemData();

    $(document).on("click", ".edit_row", function () {
        var id_ = $(this).attr("id");
        var data = parseInt($(this).attr("data"));
        fillEditValues($batch_data_set[data]);
        $("#batch_no").attr("readonly", true);
        $("#expiry").focus();
        $editMode = true;
        $createMode = false;
    })

    $(document).on("click", ".del_row", function () {
        var data_val = parseInt($(this).attr("data"));
        var r = confirm("Do you want to delete Batch: " + $batch_data_set[data_val]['batch_no']);
        if (r == true) {
            $batch_data_set[data_val]['deleted'] = 1;
            var id_ = "batch" + String(data_val);
            $("#" + id_).remove();
        } else return false;
    })

    $("#editor").submit(function (event) {
        event.preventDefault();
        $editMode = false;
        $createMode = false;
        var formdata = $(this).serializeArray();
        var data = {};
        $(formdata).each(function (index, obj) {
            data[obj.name] = obj.value;
        });

        var expiry_old = $("#expiry").val();
        if (/(([0-9][0-9])\/([2][0][0-9][0-9]))/.test(expiry_old)) {
            var yr = expiry_old.slice(3, 7);
            var month = expiry_old.slice(0, 2);
            var expiry_new = yr + "-" + month + "-" + daysInMonth(month, yr);
            data['expiry'] = expiry_new;
        }

        data['deleted'] = 0;
        if (!HandleEditItem(data)) return false; // Handle Editing in the Batch Table

        $batch_data_set.push(data);

        AddNewRow(data) // Add a new row to Table
        $uid++;
    })
})

function fillViewCompanyModal(response) {
    let company_tbody = "";
    let supplier_tbody = "";

    $.each(response, function (key, value) {
        if (key == "supplier") {
            $.each(response[key], function (key, value) {
                if (value != null) {
                    supplier_tbody += `<tr>
                    <td scope="row">${key}</td>
                    <td scope="row">${value}</td>
                </tr>`
                }
            });
        } else {
            if (value != null) {
                company_tbody += `<tr>
                <td scope="row">${key}</td>
                <td scope="row">${value}</td>
            </tr>`
            }
        }

    })
    content = `<div>\
    <table class="table table-bordered table-light 
        table-stripped table-hover table-sm table-responsive">
        <thead>
        </thead>
        <tbody>
        ${company_tbody}
        </tbody>
    </table>
    <h3 class = "text-bold">Supplier Info</h3>
    <table class="table table-bordered table-light 
        table-stripped table-hover table-sm table-responsive">
        <thead>
        </thead>
        <tbody>
        ${supplier_tbody}
        </tbody>
    </table>

    </div>`
    $("#comapny_infoModal .modal-body").html(content);

}

$("#view_company").click(function () {
    company_name = $("#id_group_id").val();
    if (company_name == "") {
        alert("No Company Name Provided");
        return false;
    }
    $("#comapny_infoModal .modal-title").text(company_name + " | INFO");
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "company_name": company_name
    };
    $.ajax({
        type: 'GET',
        url: '/company/ajax/get_company_info',
        data: data,
        beforeSend: function () {
            $(".loading").show();
        },
        complete: function () {
            $(".loading").hide();
        },

        success: function (response) {
            fillViewCompanyModal(response);
        },
        error: function (response) {
            alert("Error in resolving Company");
        }
    });
})

$("#edit_company").click(function () {
    company_name = $("#id_group_id").val();
    if (company_name == "") {
        alert("No Company Name Provided");
        return false;
    }
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "company_name": company_name
    };
    $.ajax({
        type: 'GET',
        url: '/company/ajax/get_company_id',
        data: data,
        success: function (data) {
            var url = "/company/" + data['chain_id'] + "/edit/";
            showAddEditPopup(url);
        },
        error: function (data) {
            alert("Error in resolving Company");
        }
    });
})

$("#edit_salt").click(function () {
    var salt_name = $("#id_salt_id").val();
    if (salt_name == "") {
        alert("No Salt Name Provided");
        return false;
    }
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "salt_name": salt_name
    };
    $.ajax({
        type: 'GET',
        url: '/salt/ajax/get_salt_id',
        data: data,
        success: function (data) {
            var url = "/salt/" + data['salt_id'] + "/edit/";
            showAddEditPopup(url, "Edit Salt", 450, 600);
        },
        error: function (data) {
            alert("Error in resolving edit Salt");
        }
    });
})

$("#delete").click(function () {
    var $this = $(this);
    $this.button('loading');

    var r = confirm("Are you confirm to delete this Item?");
    if (r == true) {
        var item_name = $("#id_name").val();
        var data = {
            "csrftoken": csrftoken,
            "item_name": item_name
        };
        data = JSON.stringify(data)
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            url: "/item/ajax/delete_item",
            datatype: 'json',
            data: data,
            success: function (data) {
                alert("Item is successfully Deleted");
                $this.button('reset');
                window.location = data['url'];
            },
            error: function (data) {
                $this.button('reset');
                alert("Unable to Delete Item");
            },
        });
    }
});

$(document).ready(function(){
    AutoCompleteData("/item/api/list/?format=json", "itemData", "#id_name", 30, 1)
})