var $editMode = false;
var $createMode = false;

function fill_item_table(data) {
    for (var i = 0; i < data.length; i++) {
        var id_name = "item_" + String($uid);
        var edit_id_name = "edit_" + id_name;
        var del_id_name = "del_" + id_name;

        $("#sales_table_body").append("<tr id = \'" + id_name + "\'>\
        <td class = 'item_name'>" + data[i]['item_name'] + "</td>\
        <td class = 'batch'>" + data[i]['batch_no'] + "</td>\
        <td class = 'expiry'>" + data[i]['expiry'] + "</td>\
        <td class = 'strip'>" + data[i]['strip_qty'] + "</td>\
        <td class = 'nos'>" + data[i]['nos_qty'] + "</td>\
        <td class = 'strip_free'>" + data[i]['strip_free'] + "</td>\
        <td class = 'nos_free'>" + data[i]['nos_free'] + "</td>\
        <td class = 'mrp'>" + data[i]['rate'] + "</td>\
        <td class = 'amt'>" + data[i]['amount'] + "</td>\
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
    document.getElementById("Item-sale-form").reset();

    $("#item-sale-modal-editor").modal("toggle");

    $("#id_item_id").val(dataJson['item_name']);
    $("#id_batch_no").val(dataJson['batch_no']);

    var expiry = dataJson['expiry'];
    expiry = expiry.slice(5, 7) + "/" + expiry.slice(0, 4);
    $("#expiry").val(expiry);

    $("#id_strip_qty").val(dataJson['strip_qty']);
    $("#id_nos_qty").val(dataJson['nos_qty']);
    $("#id_strip_free").val(dataJson['strip_free']);
    $("#id_nos_free").val(dataJson['nos_free']);

    $("#id_purchase").val(parseFloat(dataJson['pur_rate']));
    $("#id_sales").val(parseFloat(dataJson['mrp']));
    $("#id_unit").val(dataJson['conv']);
    $("#id_discount").val(parseFloat(dataJson['discount']));

    $("#id_sgst").val(dataJson['sgst']);
    $("#id_cgst").val(dataJson['cgst']);
    $("#id_sgst_type").val(dataJson['sgst_type']);
    $("#id_cgst_type").val(dataJson['cgst_type']);

    $("#id_disc_type").val(dataJson['disc_type']);
    $("#id_other_charge").val(dataJson['other_charge']);
    $("#id_amount").val(parseFloat(dataJson['amount']));

    $("#strip_stock").val(parseFloat(dataJson['strip_stock']));
    $("#nos_stock").val(parseFloat(dataJson['nos_stock']));

}

function HandleEditItem(data) {
    for (var i = 0; i < parseInt($item_data_set.length); i++) {

        if ($item_data_set[i] != null && data['item_name'] == $item_data_set[i]['item_name'] &&
            data['batch_no'] == $item_data_set[i]['batch_no'] && $item_data_set[i]['deleted'] != 1) {

            $item_data_set[i]['strip_qty'] = data['strip_qty'];
            $item_data_set[i]['strip_free'] = data['strip_free'];
            $item_data_set[i]['rate'] = data['rate'];
            $item_data_set[i]['pur_rate'] = data['purchase_Rate'];
            $item_data_set[i]['other_charge'] = data['other_charge'];
            $item_data_set[i]['nos_qty'] = data['nos_qty'];
            $item_data_set[i]['nos_free'] = data['nos_free'];
            $item_data_set[i]['mrp'] = data['mrp'];
            $item_data_set[i]['discount'] = data['discount'];
            $item_data_set[i]['disc_type'] = data['disc_type'];
            $item_data_set[i]['cgst'] = data['cgst'];
            $item_data_set[i]['sgst'] = data['sgst'];

            var old_amt = parseFloat($item_data_set[i]['amount']);
            var new_amt = parseFloat(data['amount']);
            populate_amount(true, old_amt, new_amt);
            $item_data_set[i]['amount'] = data['amount'];

            var old_cgst_amt = parseFloat($item_data_set[i]['cgst_amt']);
            var new_cgst_amt = parseFloat(data['cgst_amt']);
            var old_sgst_amt = parseFloat($item_data_set[i]['sgst_amt']);
            var new_sgst_amt = parseFloat(data['sgst_amt']);
            populate_gst(true, old_sgst_amt, new_sgst_amt, old_cgst_amt, new_cgst_amt);
            $item_data_set[i]['cgst_amt'] = data['cgst_amt'];
            $item_data_set[i]['sgst_amt'] = data['sgst_amt'];

            var row_id = "#item_" + String(i);
            $(row_id + " > .strip").html(data['strip_qty']);
            $(row_id + " > .nos").html(data['nos_qty']);
            $(row_id + " > .strip_free").html(data['strip_free']);
            $(row_id + " > .nos_free").html(data['nos_free']);
            $(row_id + " > .mrp").html(data['mrp']);
            $(row_id + " > .amt").html(data['amount']);

            return false;
        }
    }
    return true;
}

function populate_amount(is_edit, item_amount_old, item_amount_new) {
    // setting Sale form Item Amount and Net Amounnt
    var item_amt = parseFloat($("#id_amount").val());
    var total_amt = parseFloat($("#id_rec_amt").val());
    var net_amt = parseFloat($("#id_net_amount").val());
    if (is_edit == true) {
        total_amt = total_amt - item_amount_old + item_amount_new;
    } else {
        total_amt += item_amt;
    }

    $("#id_rec_amt").val(total_amt.toFixed(2));
    $("#id_net_amount").val(total_amt.toFixed(2));
}

function populate_gst(is_edit, old_sgst, new_sgst, old_cgst, new_cgst) {
    // setting Sale form Item Amount and Net Amounnt
    var net_sgst = parseFloat($("#id_net_sgst").val());
    var net_cgst = parseFloat($("#id_net_cgst").val());

    if (is_edit == true) {
        net_sgst = net_sgst - old_sgst + new_sgst;
        net_cgst = net_cgst - old_cgst + new_cgst;
    } else {
        net_sgst += new_sgst;
        net_cgst += new_cgst;
    }

    $("#id_net_sgst").val(net_sgst.toFixed(2));
    $("#id_net_cgst").val(net_cgst.toFixed(2));
    $("#id_net_gst").val((net_cgst + net_sgst).toFixed(2));
}

function CheckTotalAmt() {
    var expected_amt = 0.00;
    $.each($item_data_set, function (i, row) {
        if (row["deleted"] == 0)
            expected_amt += parseFloat(row['amount']);
    });
    expected_amt = expected_amt.toFixed(2);
    var amt_spec = $("#id_net_amount").val();
    amt_spec = parseFloat(amt_spec);
    amt_spec = amt_spec.toFixed(2);
    if (amt_spec != expected_amt) {
        var r = confirm("Amount Mismatch!! Correct the amount?");
        if (r == true) {
            $("#id_net_amount").val(expected_amt);
            $("#id_rec_amt").val(expected_amt);
        } else {
            return false;
        }
    }
}

function get_sales_info_for_save() {
    var sale_info = {};
    var key, value;
    $('input, select').each(function () {
        key = $(this).attr("name");
        if (key != "csrfmiddlewaretoken" && key != "initial-doc_dt") {
            sale_info[key] = $(this).val();
        }
        if (key == "doc_dt") {
            var regex = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/;
            var expiry = $(this).val();
            if (regex.test(expiry)) {
                expiry = expiry.slice(6, 10) + "-" + expiry.slice(0, 2) + "-" + expiry.slice(3, 5);
                sale_info[key] = expiry;
            }
        }
        if (key == "net_amount") {
            return false;
        }
    });
    return sale_info;
}

$("#delete").click(function () {
    var $this = $(this);
    $this.button('loading');
    var r = confirm("Are you confirm to delete this Invoice?");
    if (r == true) {
        var doc_no = $("#id_doc_no").val();
        var data = {
            "csrftoken": csrftoken,
            "doc_no": doc_no
        };
        data = JSON.stringify(data)
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            url: "/sales/ajax/delete_inv",
            datatype: 'json',
            data: data,
            success: function (data) {
                $this.button('reset');
                alert("Sale Invoice is successfully Deleted");
                window.location = data['url']
            },
            error: function (data) {
                $this.button('reset');
                alert("Error in Deletion")
            }
        });
    }
    CheckTotalAmt();
});


function AddNewRow(data) {
    var id_name = "item_" + $uid;
    var edit_id_name = "edit_" + id_name;
    var del_id_name = "del_" + id_name;

    $("#sales_table_body").append("<tr id  = \'" + id_name + "\'>\
    <td class = 'item_name'>" + data['item_name'] + "</td>\
    <td class = 'batch'>" + data['batch_no'] + "</td>\
    <td class = 'expiry'>" + data['expiry'] + "</td>\
    <td class = 'strip'>" + data['strip_qty'] + "</td>\
    <td class = 'nos'>" + data['nos_qty'] + "</td>\
    <td class = 'strip_free'>" + data['strip_free'] + "</td>\
    <td class = 'nos_free'>" + data['nos_free'] + "</td>\
    <td class = 'mrp'>" + data['mrp'] + "</td>\
    <td class = 'amt'>" + data['amount'] + "</td>\
    <td class = 'buttons'>\
        <button data = \'" + $uid + "\' class = 'edit_row' id = \'" + edit_id_name + "\'>\
            <span class='glyphicon glyphicon-edit' aria-hidden='true'></span></button>\
            <button data = \'" + $uid + "\' class = 'del_row' id = \'" + del_id_name + "\'>\
                <span class='glyphicon glyphicon-trash' aria-hidden='true'></span></button></button>\
            </td></tr>")
}



$("#id_nos_qty, #id_strip_qty").blur(function () {
    if ($createMode) {
        var batch = $("#id_batch_no").val();
        var itemName = $("#id_item_id").val();
        for (var i = 0; i < parseInt($item_data_set.length); i++) {
            if (itemName == $item_data_set[i]['item_name'] && batch == $item_data_set[i]['batch_no'] && batch != "" && $item_data_set[i]['deleted'] != 1) {
                $('#item-sale-modal-editor').modal('toggle');
                alert("Same Item/Batch not allowed");
                return false;
            }
        }
    }
})


$("#id_item_id").blur(function () {
    if ($("#item_id_field").val() == "") {
        $("#id_batch_no").focus();
        alert("Item not selected. Try again");
        $(this).val("");
    }
})



function SubmitValidation() {
    var strip = $("#id_strip_qty").val();
    var nos = $("#id_nos_qty").val();
    var mrp = $("#id_sales").val();
    var free_strip = $("#id_strip_free").val();
    var nos_free = $("#id_nos_free").val();
    var amt = $("#id_amount").val();
    var purchase = $("#id_purchase").val();
    var discount = $("#id_discount").val();
    var other_charge = $("#id_other_charge").val();

    if (strip == "") $("#id_strip_qty").val(0);
    if (nos == "") $("#id_nos_qty").val(0);
    if (free_strip == "") $("#id_strip_free").val(0);
    if (nos_free == "") $("#id_nos_free").val(0);
    if (mrp == "") $("#id_sales").val(0.00);
    if (amt == "") $("#id_amount").val(0.00);
    if (purchase == "") $("#id_purchase").val(0.00);
    if (discount == "") $("#id_discount").val(0.00);
    if (other_charge == "") $("#id_other_charge").val(0.00);

    if (strip == 0 && nos == 0) {
        alert("Please add qty");
        $("#id_nos_qty").focus();
        return false;
    }
    if (mrp == 0) {
        alert("Mrp cannot be nil");
        $("#id_sales").focus();
        return false;
    }
    if (amt == 0) {
        alert("Amount cannot be nil");
        $("#id_item_id").focus();
        return false;
    }
    return true;
}


$("#id_strip_free,  #id_nos_free, #id_sales").focus(function () {
    NosConversionStrip();
})

//Handling Discount and Excise, Other Charges

function manageItemAmount(params) {
    var mrp = parseFloat($("#id_sales").val());
    var disc_type = $("#id_disc_type option:selected").text();
    var disc = parseFloat($("#id_discount").val());
    var other_charge = parseFloat($("#id_other_charge").val());
    var conv = parseInt($("#id_unit").val());
    var strip = parseInt($("#id_strip_qty").val());
    var nos = parseInt($("#id_nos_qty").val());

    var amount = mrp * (strip + nos / conv);

    if (disc) {
        if (disc_type == "%") amount -= amount * (disc / 100);
        if (disc_type == "Rs") amount -= disc;
    }
    if (other_charge) amount += other_charge;

    $("#id_amount").val(amount.toFixed(2));
}

$("#id_amount").blur(function () {
    manageItemAmount();
})


$("#id_nos_qty").blur(function (e) {
    var expiry = $("#expiry").val();
    if (expiry == "") {
        alert("Expiry can't be blank");
        $("#expiry").focus();
        return false;
    }

    var strip = $("#id_strip_qty").val();
    var nos = $("#id_nos_qty").val();

    if (strip == "")
        $("#id_strip_qty").val(0);
    if (nos == "")
        $("#id_nos_qty").val(0);

    var conv = parseInt($("#id_unit").val());
    var total_qty = strip * conv + nos;

    var strip_stock = parseInt($("#strip_stock").val());
    var nos_stock = parseInt($("#nos_stock").val());
    var total_available_qty = strip_stock * conv + nos_stock;

    if (total_qty > total_available_qty) {
        e.stopImmediatePropagation();
        e.preventDefault();
        var r = confirm("Nagetive Sales Goes On!");
        if (r == true) {
            $("#id_nos_free").focus();
            $(this).data('bs.modal', null);
        } else {
            $("#id_strip_qty").val(0);
            $("#id_nos_qty").val(0);
            $("#id_strip_qty").focus();
        }
    }
    if ((strip == 0 && nos == 0) || strip + nos == 0) {
        alert("Please enter some qty");
        $("#id_strip_qty").focus();
    }
    return false;
})



$("#expiry").blur(function () {
    expiryValidations();
})

$(".modal-wide").on("show.bs.modal", function () {
    var height = $(window).height() - 150;
    $(this).find(".modal-body").css("max-height", height);
});

$("#id_doc_no").attr("readonly", "readonly");

$(document).on('keypress', "#sale-item-submit", function (e) {
    if (e.which == 13) {
        e.preventDefault();
        $("#sale-item-submit").click();
    }
});
//For use enter to go to next field
$(document).on('keypress', "input:not( :disabled, .main-btn, #id_message), select", function (e) {
    if (e.which == 13) {
        e.preventDefault();
        var index = $("select:enabled, input:not( :disabled, .main-btn), input[type='search']").index(this) + 1;
        $("select:enabled, input:not( :disabled, .main-btn), input[type='search']").eq(index).focus();
    }
});
$(document).on('keypress', "button, input:not([readonly], :disabled, .main-btn, #id_item_id, #id_party_id), select", function (e) {
    if (e.shiftKey && e.which == 13) {
        e.preventDefault();
        var index = $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").index(this) - 1;
        $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").eq(index).focus();
    }
});


$("#search_inv_btn").click(function () {
    var sale_inv = $('#search_inv_input').val();
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "sale_inv": sale_inv
    };
    $.ajax({
        type: 'GET',
        url: '/sales/ajax/search_inv',
        data: data,
        beforeSend: function () {
            $(".loading").show();
            $("#sale_inv_search").toggle();
        },
        complete: function () {
            $(".loading").hide();
        },
        success: function (data) {
            if (parseInt(data['status']) == 1) {
                location.href = data['msg']
            } else {
                $("#sale_inv_search").toggle();
                $("#search_inv_input").focus();
                $("#seearch_error").css("display", "inline");
            }
        },
        error: function (data) {
            $("#sale_inv_search").toggle();
            $("#search_inv_input").focus();
            $("#seearch_error").css("display", "inline");
        }
    });
})


$("#id_batch_no").attr("required", true);
//add attr of only positive integer
$("#id_strip_qty").attr("min", 0);
$("#id_nos_qty").attr("min", 0);
$("#id_strip_free").attr("min", 0);
$("#id_nos_free").attr("min", 0);

$("#id_discount").attr("min", 0.00);
$("#id_sales").attr("min", 0.00);
$("#id_amount").attr("min", 0.00);
$("#id_purchase").attr("min", 0.00);
$("#id_other_charge").attr("min", 0.00);
$("#id_amount").attr("readonly", "readonly");
$("#id_amount").css("color", "#6C6E71");
$("#id_doc_dt").attr("type", "date");

/*$("#id_rec_amt, #id_net_amount").attr("readonly", "readonly");*/
$("#id_rec_amt, #id_net_amount").css("background-color", "#FCF3CF");


//convert nos to strip if more than conv
function NosConversionStrip() {

    var strip = parseInt($("#id_strip_qty").val());
    var nos = parseInt($("#id_nos_qty").val());
    var conv = parseInt($("#id_unit").val());
    var total_qty = strip * conv + nos;
    if (nos / conv >= 1) {
        strip = strip + Math.floor(nos / conv);
        $("#id_strip_qty").val(strip);
        $("#id_nos_qty").val(nos % conv);
    }
    return total_qty;
}
//change the value of total amount aND net amount

function get_salesinfo_for_print() {
    var sale_info = {};
    sale_info['total_item'] = $item_data_set.length;
    sale_info['sale_discount'] = $("#id_sale_discount").val();
    sale_info['sale_adjustment'] = $("#id_sale_adjustment").val();
    sale_info['net_amount'] = $("#id_net_amount").val();
    sale_info['party_id'] = $("#id_party_id").val();
    sale_info['inv_no'] = $("#id_doc_no").val();
    sale_info['doctor_id'] = $("#id_doctor_id").val();
    sale_info['doc_dt'] = $("#id_doc_dt").val();
    sale_info['gst'] = $("#id_net_gst").val();
    return sale_info;
}

function get_item_table_for_print() {
    var sale_item = [];
    var item = {};
    for (var i = 0; i < $item_data_set.length; i++) {
        item = {};
        var strip = parseInt($item_data_set[i]['strip_qty']) + parseInt($item_data_set[i]['strip_free']);
        var nos = parseInt($item_data_set[i]['nos_qty']) + parseInt($item_data_set[i]['nos_free']);
        var conv = parseInt($item_data_set[i]['conv']);
        var qty = strip * conv + nos;
        item['item_name'] = $item_data_set[i]['item_name'];
        item['batch'] = $item_data_set[i]['batch_no'];
        item['amount'] = $item_data_set[i]['amount'];
        item['expiry'] = $item_data_set[i]['expiry'];
        item['mrp'] = $item_data_set[i]['mrp'];
        item['qty'] = qty;
        sale_item.push(item);
    }
    return sale_item;
}
$("#view_inv").click(function () {
    var $this = $(this);
    $this.button('loading');

    var sale_info = get_salesinfo_for_print();
    var sale_item = get_item_table_for_print();
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "sale_info": sale_info,
        "sale_item": sale_item
    };
    data = JSON.stringify(data);
    $.ajax({
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        url: "/sales/view_invoice",
        datatype: 'json',
        data: data,
        complete: function () {
            $this.button('reset');
        },
        success: function (data) {
            if (data['status'] == 0) {
                $this.button('reset');
                alert("Something went wrong");
            }
        },
        errors: function (data) {
            $this.button('reset');
            alert("Something went wrong");
        }
    })
})

$("#print_inv").click(function () {
    var $this = $(this);
    $this.button('loading');

    var sale_info = get_salesinfo_for_print();
    var sale_item = get_item_table_for_print();
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "sale_info": sale_info,
        "sale_item": sale_item
    };
    data = JSON.stringify(data);
    $.ajax({
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        url: "/sales/print_invoice",
        datatype: 'json',
        data: data,
        complete: function () {
            $this.button('reset');
        },

        success: function (data) {
            $this.button('reset');
            if (data['status'] == 0) {
                alert(data['msg']);
            }
        },
        errors: function (data) {
            $this.button('reset');
            alert("Something went wrong");
        }
    })
})

$("#edit_doctor").click(function () {
    doctor_name = $("#id_doctor_id").val();
    if (doctor_name == "") {
        alert("No Doctor Name Provided");
        return false;
    }
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "doctor_name": doctor_name
    };
    $.ajax({
        type: 'GET',
        url: '/sales/doctor/ajax/get_doctor_id',
        data: data,
        success: function (data) {
            var url = "/sales/doctor/" + data['doctor_id'] + "/edit/";
            showAddEditPopup(url);
        },
        error: function (data) {
            alert("Error in resolving Doctor");
        }
    });
})

$(document).ready(function () {
    $(".sales").addClass("active");
    $("#add_doctor, #edit_doctor").click(function () {
        localStorage.removeItem("doctorData");
    })

    $(document).on("click", ".edit_row", function () {
        var id_ = $(this).attr("id");
        var data = parseInt($(this).attr("data"));
        fillEditValues($item_data_set[data]);
        $("#id_batch_no").attr("readonly", true);
        $("#id_item_id").attr("readonly", true);
        $("#id_nos_qty").focus();
        $createMode = false;
        $editMode = true;
    })

    $(document).on("click", ".del_row", function () {
        var data_val = parseInt($(this).attr("data"));
        var r = confirm("Do you want to delete item: " + $item_data_set[data_val]['item_name']);
        if (r == true) {
            var deleted_item_amt = parseFloat($item_data_set[data_val]['amount']);
            var total_amt = parseFloat($("#id_rec_amt").val()) - deleted_item_amt;
            $("#id_rec_amt").val(total_amt.toFixed(2));
            $("#id_net_amount").val(total_amt.toFixed(2));
            var deleted_item_cgst_amt = parseFloat($item_data_set[data_val]['cgst_amt']);
            var total_cgst_amt = parseFloat($("#id_net_cgst").val()) - deleted_item_cgst_amt;
            $("#id_net_cgst").val(total_cgst_amt.toFixed(2));

            var deleted_item_sgst_amt = parseFloat($item_data_set[data_val]['sgst_amt']);
            var total_sgst_amt = parseFloat($("#id_net_sgst").val()) - deleted_item_sgst_amt;
            $("#id_net_sgst").val(total_sgst_amt.toFixed(2));
            $("#id_net_gst").val((total_sgst_amt + total_cgst_amt).toFixed(2));
            $item_data_set[data_val]['deleted'] = 1;
            var id_ = "item_" + String(data_val);
            $("#" + id_).remove();
        } else {
            return false;;
        }
    })

    $("#sale-item-submit").focus(function () {
        manageItemAmount();
        NosConversionStrip();
        expiryValidations();
        SubmitValidation();
    })
    // Submit the Dtl form
    $("#Item-sale-form").submit(function (event) {
        event.preventDefault();
        $createMode = false;
        $editMode = false;

        $("#item-sale-modal-editor").modal("hide");

        // if ( !SubmitValidation() ) return false;
        var formdata = $(this).serializeArray();
        var data = {};
        $(formdata).each(function (index, obj) {
            data[obj.name] = obj.value;
        });
        fillItemEntryData(data);

        if (!HandleEditItem(data)) return false; // Handle Editing in Dtl Item Table

        populate_amount(false, 0, parseFloat(data['amount']));
        populate_gst(false, 0, parseFloat(data['cgst_amt']), 0, parseFloat(data['sgst_amt']));

        AddNewRow(data); // Add a new row to Table
        $item_data_set.push(data);
        $uid++;
    })

})

function fillItemEntryData(data) {
    data['item_name'] = $("#id_item_id").val();

    data['item_id'] = $("#item_id_field").val();
    data['conv'] = $("#id_unit").val();
    data['rate'] = $("#id_sales").val();
    data['pur_rate'] = $("#id_purchase").val();
    data['strip_stock'] = $("#strip_stock").val();
    data['nos_stock'] = $("#nos_stock").val();
    data['cgst'] = $("#id_cgst").val();
    data['sgst'] = $("#id_sgst").val();
    data['deleted'] = 0;
    var amount = parseFloat(data['amount']);
    var cgst_amt = data['cgst_amt'] = (parseFloat(data['cgst'] / 100) * amount).toFixed(2);
    var sgst_amt = data['sgst_amt'] = (parseFloat(data['sgst'] / 100) * amount).toFixed(2);

    var expiry_old = $("#expiry").val();

    if (/(([0-9][0-9])\/([2][0][0-9][0-9]))/.test(expiry_old)) {
        var yr = expiry_old.slice(3, 7);
        var month = expiry_old.slice(0, 2);
        var expiry_new = yr + "-" + month + "-" + daysInMonth(month, yr);
        data['expiry'] = expiry_new;
    }
    return data;
}


function saveUpdateMethod(url) {
    $('#save, #update').click(function (e) {
        var $this = $(this);
        $this.button('loading');
        if ($("#id_party_id").val() == "") {
            alert("Patient name is required\n");
            $this.button('reset');
            return false;
        }
        if (this.id == 'save')
            if (this.id == 'update')
                $("#edot_ajax_loading").css("display", "inline");

        var total_disc = parseFloat($("#id_sale_disc_type").val());
        var total_disc_type = $("#id_sale_disc_type option:selected").val();
        var sale_adjustment = parseFloat($("#id_sale_adjustment").val());

        var net_amt = parseFloat($("#id_net_amount").val());

        if (total_disc) {
            if (total_disc_type == "%") net_amt -= total_disc * (net_amt / 100);
            else net_amt -= total_disc;
        }
        if (sale_adjustment) net_amt += sale_adjustment;
        $("#id_net_amount").val(net_amt.toFixed(2));

        //----------------------------------------------------------------------------//
        //validation of form SaleInvDtl
        CheckTotalAmt();
        //Taking all the values of form Sale InvHrd
        e.preventDefault();
        var sale_info = get_sales_info_for_save();

        var data = {
            "csrfmiddlewaretoken": csrftoken,
            "sale_info": sale_info,
            "item_table": $item_data_set
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
                if (data.status == "500")
                    alert("Something went wrong. Contact Jai");
                try {
                    var errors = data.responseJSON.errors;
                    if (errors.length) {
                        for (i = 0; i < errors.length; i++) {
                            $.each(errors[i], function (key, key_error_arr) {
                                var key_errors = "";
                                for (i = 0; i < key_error_arr.length; i++) {
                                    key_errors += key_error_arr[i]; + ", ";
                                }
                                if (data.responseJSON.item)
                                    alert("In item " + data.responseJSON.item + ", " + key + " has error : " + key_errors);
                                else
                                    alert(key + " : " + key_errors);
                                return false;
                            });
                        }
                    } else
                        alert(errors);
                } catch (err) {
                    alert(data.responseText);
                }
            }
        });
        $("#edit_ajax_loading").css("display", "none");
    }); //end of save function
}

$("#search").click(function(){
    $("#sale_inv_search").modal("toggle");
    $("#search_inv_input").focus();
    $("#search_inv_input").val("");
    $("#seearch_error").css("display", "none");
})
$("#search_inv_input").focus(function(){
    $(document).on('keypress', "#search_inv_input", function (e) {
        if (e.which == 13) {
            e.preventDefault();
            $("#search_inv_btn").click();
        }
    })

});