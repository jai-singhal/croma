var $editMode = false;
var $createMode = false;

function fill_item_table(data) {
    for (var i = 0; i < data.length; i++) {
        var id_name = "item_" + String($uid);
        var edit_id_name = "edit_" + id_name;
        var del_id_name = "del_" + id_name;
        var free_qty = parseInt(data[i]['strip_free']) * parseInt(data[i]['conv']) + parseInt(data[i]['nos_free']);
        var qty = parseInt(data[i]['strip_qty']) * parseInt(data[i]['conv']) + parseInt(data[i]['nos_qty']);
        $("#purchase_table_body").append("<tr id = \'" + id_name + "\'>\
        <td class = 'item_name'>" + data[i]['item_name'] + "</td>\
        <td class = 'batch'>" + data[i]['batch_no'] + "</td>\
        <td class = 'expiry'>" + data[i]['expiry'] + "</td>\
        <td class = 'total_qty'>" + qty + "</td>\
        <td class = 'qty_free'>" + free_qty + "</td>\
        <td class = 'mrp'>" + data[i]['mrp'] + "</td>\
        <td class = 'rate'>" + data[i]['rate'] + "</td>\
        <td class = 'discount'>" + data[i]['discount'] + "</td>\
        <td class = 'sgst'>" + data[i]['sgst'] + "</td>\
        <td class = 'cgst'>" + data[i]['cgst'] + "</td>\
        <td class = 'amt'>" + data[i]['amount'] + "</td>\
        <td class ='buttons'>\
            <button data = \'" + $uid + "\' class = 'edit_row' id = \'" + edit_id_name + "\'>\
                <span class='glyphicon glyphicon-edit' aria-hidden='true'></span></button>\
            <button data = \'" + $uid + "\' class = 'del_row' id = \'" + del_id_name + "\'>\
                <span class='glyphicon glyphicon-trash' aria-hidden='true'></span></button></button>\
        </td></tr>")
        $uid++;
    }
}

function AddNewRow(data) {
    var id_name = "item_" + $uid;
    var edit_id_name = "edit_" + id_name;
    var del_id_name = "del_" + id_name;
    var free_qty = parseInt(data['strip_free']) * parseInt(data['conv']) + parseInt(data['nos_free']);
    var qty = parseInt(data['strip_qty']) * parseInt(data['conv']) + parseInt(data['nos_qty']);
    $("#purchase_table_body").append("<tr id  = \'" + id_name + "\'>\
        <td class = 'item_name'>" + data['item_name'] + "</td>\
        <td class = 'batch'>" + data['batch_no'] + "</td>\
        <td class = 'expiry'>" + data['expiry'] + "</td>\
        <td class = 'total_qty'>" + qty + "</td>\
        <td class = 'qty_free'>" + free_qty + "</td>\
        <td class = 'mrp'>" + data['mrp'] + "</td>\
        <td class = 'rate'>" + data['rate'] + "</td>\
        <td class = 'discount'>" + data['discount'] + "</td>\
        <td class = 'sgst'>" + data['sgst'] + "</td>\
        <td class = 'cgst'>" + data['cgst'] + "</td>\
        <td class = 'amt'>" + data['amount'] + "</td>\
        <td class ='buttons'>\
            <button data = \'" + $uid + "\' class = 'edit_row' id = \'" + edit_id_name + "\'>\
                <span class='glyphicon glyphicon-edit' aria-hidden='true'></span></button>\
            <button data = \'" + $uid + "\' class = 'del_row' id = \'" + del_id_name + "\'>\
                <span class='glyphicon glyphicon-trash' aria-hidden='true'></span></button></button>\
        </td></tr>")
}

function SubmitValidation1() {
    var strip = $("#id_strip_qty").val();
    var nos = $("#id_nos_qty").val();
    var mrp = $("#id_sales").val();
    var free_strip = $("#id_strip_free").val();
    var nos_free = $("#id_nos_free").val();
    var amt = $("#id_amount").val()
    if (strip == "") $("#id_strip_qty").val(0);
    if (nos == "") $("#id_nos_qty").val(0);
    if (free_strip == "") $("#id_strip_free").val(0);
    if (nos_free == "") $("#id_nos_free").val(0);
    if (mrp == "") $("#id_sales").val(0.00);
    if (amt == "") $("#id_amount").val(0.00);
    if (strip == 0 && nos == 0) {
        alert("Please add Some Item");
        return false;
    }
    if (amt == 0) {
        alert("Amount cannot be Nill");
        return false;
    }
    return true;
}

function fillEditValues(dataJson) {
    document.getElementById("Item-purchase-form").reset();

    $("#item-purchase-modal-editor").modal("toggle");

    $("#id_item_id").val(dataJson['item_name']);
    $("#id_batch_no").val(dataJson['batch_no']);

    var expiry = dataJson['expiry'];
    expiry = expiry.slice(5, 7) + "/" + expiry.slice(0, 4);
    $("#expiry").val(expiry);

    $("#id_strip_qty").val(dataJson['strip_qty']);
    $("#id_nos_qty").val(dataJson['nos_qty']);
    $("#id_strip_free").val(dataJson['strip_free']);
    $("#id_nos_free").val(dataJson['nos_free']);

    $("#id_purchase").val(parseFloat(dataJson['rate']));
    $("#id_sales").val(parseFloat(dataJson['mrp']));
    $("#id_unit").val(dataJson['conv']);

    $("#id_inst_rate").val(dataJson['inst_rate']);
    $("#id_mrp").val(dataJson['mrp']);
    $("#id_trade_rate").val(dataJson['trade_rate']);
    $("#id_std_rate").val(dataJson['std_rate']);

    $("#id_sgst").val(dataJson['sgst']);
    $("#id_cgst").val(dataJson['cgst']);
    $("#id_sgst_type").val(dataJson['sgst_type']);
    $("#id_cgst_type").val(dataJson['cgst_type']);

    $("#id_discount").val(parseFloat(dataJson['discount']));
    $("#id_disc_type").val(dataJson['disc_type']);
    $("#id_excise").val(parseFloat(dataJson['excise']));
    $("#id_excise_type").val(dataJson['excise_type']);
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
            $item_data_set[i]['other_charge'] = data['other_charge'];
            $item_data_set[i]['nos_qty'] = data['nos_qty'];
            $item_data_set[i]['nos_free'] = data['nos_free'];

            $item_data_set[i]['strip_pur'] = data['strip_pur'];
            $item_data_set[i]['strip_sale'] = data['strip_sale'];

            $item_data_set[i]['rate'] = data['rate'];
            $item_data_set[i]['excise_type'] = data['excise_type'];
            $item_data_set[i]['excise'] = data['excise'];
            $item_data_set[i]['discount'] = data['discount'];

            $item_data_set[i]['inst_rate'] = data['inst_rate'];
            $item_data_set[i]['mrp'] = data['mrp'];
            $item_data_set[i]['trade_rate'] = data['trade_rate'];
            $item_data_set[i]['std_rate'] = data['std_rate'];

            $item_data_set[i]['cgst'] = data['cgst'];
            $item_data_set[i]['sgst'] = data['sgst'];

            $item_data_set[i]['disc_type'] = data['disc_type'];
            //change in item table
            var old_amt = parseFloat($item_data_set[i]['amount']);
            var new_amt = parseFloat(data['amount']);

            populate_amount(true, old_amt, new_amt);
            $item_data_set[i]['amount'] = data['amount'];

            var old_disc_amt = parseFloat($item_data_set[i]['disc_amt']);
            var new_disc_amt = parseFloat(data['disc_amt']);
            populate_less_disc(true, old_disc_amt, new_disc_amt)
            $item_data_set[i]['disc_amt'] = data['disc_amt'];

            var taxable = data['taxable'] = AdjustAmount() - new_disc_amt;

            var old_cgst_amt = parseFloat($item_data_set[i]['cgst_amt']);
            var new_cgst_amt = parseFloat(data['cgst_amt']);
            var old_sgst_amt = parseFloat($item_data_set[i]['sgst_amt']);
            var new_sgst_amt = parseFloat(data['sgst_amt']);
            populate_gst(true, old_sgst_amt, new_sgst_amt, old_cgst_amt, new_cgst_amt);
            $item_data_set[i]['cgst_amt'] = data['cgst_amt'];
            $item_data_set[i]['sgst_amt'] = data['sgst_amt'];


            var free_qty = parseInt(data['strip_free']) * parseInt(data['conv']) + parseInt(data['nos_free']);

            var qty = parseInt(data['strip_qty']) * parseInt(data['conv']) + parseInt(data['nos_qty']);
            var row_id = "#item_" + String(i);
            $(row_id + " > .expiry").html(data['expiry']);
            $(row_id + " > .total_qty").html(qty);
            $(row_id + " > .qty_free").html(free_qty);
            $(row_id + " > .mrp").html(data['mrp']);
            $(row_id + " > .rate").html(data['rate']);
            $(row_id + " > .discount").html(data['discount']);
            $(row_id + " > .sgst").html(data['sgst']);
            $(row_id + " > .cgst").html(data['cgst']);
            $(row_id + " > .amt").html(data['amount']);

            return false;
        }
    }
    return true;
}

function populate_less_disc(is_edit, item_disc_old, item_disc_new) {
    // setting Sale form Item Amount and Net Amounnt
    var total_disc = parseFloat($("#id_net_discount").val());

    if (is_edit == true) {
        total_disc = total_disc - item_disc_old + item_disc_new;
    } else {
        total_disc += item_disc_new;
    }

    $("#id_net_discount").val(total_disc.toFixed(2));
}

function populate_amount(is_edit, item_amount_old, item_amount_new) {
    // setting Sale form Item Amount and Net Amounnt
    var item_amt = parseFloat($("#id_amount").val());
    var net_total_amt = parseFloat($("#id_net_amount").val());

    if (is_edit == true) {
        net_total_amt = net_total_amt - item_amount_old + item_amount_new;
    } else {
        net_total_amt += item_amt;
    }

    $("#id_net_amount").val(net_total_amt.toFixed(2));
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
}

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

function AdjustAmount() {
    var rate = parseFloat($("#id_purchase").val());
    var conv = parseInt($("#id_unit").val());
    var strip = parseInt($("#id_strip_qty").val());
    var nos = parseInt($("#id_nos_qty").val());
    var amount = rate * (strip + nos / conv);
    return amount;
}


//add attr of only positive integer
$("#id_strip_qty").attr("min", 0);
$("#id_nos_qty").attr("min", 0);
$("#id_strip_free").attr("min", 0);
$("#id_nos_free").attr("min", 0);

$("#id_discount").attr("min", 0.00);
$("#id_sales").attr("min", 0.00);
$("#id_amount").attr("min", 0.00);
$("#id_excise").attr("min", 0.00);
$("#id_purchase").attr("min", 0.00);
$("#id_other_charge").attr("min", 0.00);
$("#id_amount").attr("readonly", "readonly");
$("#id_amount").css("color", "#6C6E71");
$("#id_doc_dt").attr("type", "date");

$("#id_net_discount").attr("readonly", "readonly").css("background-color", "#FCF3CF");;
$("#id_net_cgst").attr("readonly", "readonly").css("background-color", "#FCF3CF");
$("#id_net_sgst").attr("readonly", "readonly").css("background-color", "#FCF3CF");
$("#id_net_amount").attr("readonly", "readonly").css("background-color", "#FCF3CF");
$("#id_net_adj").attr("readonly", "readonly").css("background-color", "#FCF3CF");


$("#edit_supplier").click(function () {
    supplier_name = $("#id_supplier_id").val();
    if (supplier_name == "") {
        alert("No Supplier Name Provided");
        return false;
    }
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "supplier_name": supplier_name
    };
    $.ajax({
        type: 'GET',
        url: '/company/ajax/get_supplier_id',
        data: data,
        success: function (data) {
            var url = "/company/supplier/" + data['supplier_id'] + "/edit/";
            showAddEditPopup(url);
        },
        error: function (data) {
            alert("Error in resolving Supplier");
        }
    });
})

$("#id_paid_sgst").blur(function () {
    var sgst = parseFloat($(this).val());
    var cgst = parseFloat($("#id_paid_cgst").val());
    if (cgst != sgst && cgst != 0) {
        $("#id_paid_cgst").val(0.00);
        $(this).val(0.00);
        alert("CGST and SGST must be equal");
        $("#id_paid_cgst").focus();
    } else {
        $("#id_paid_cgst").val(cgst.toFixed(2));
        $(this).val(sgst.toFixed(2));
    }
    var disc = parseFloat($("#id_paid_discount").val()).toFixed(2);
    $("#id_paid_discount").val(disc);
});

$("#id_paid_discount").blur(function () {
    var disc = $("#id_paid_discount").val();
    if (disc == "")
        $("#id_paid_discount").val(0.00);
});


$("#id_paid_amount").blur(function () {
    checkSuppAndInvDuplicate();
    var paid_amt = $("#id_paid_amount").val();
    if (paid_amt == "")
        $("#id_paid_amount").val(0.00);
});


$("#id_nos_qty, #id_strip_qty").blur(function () {
    if ($createMode) {
        var batch = $("#id_batch_no").val();
        var itemName = $("#id_item_id").val();
        for (var i = 0; i < parseInt($item_data_set.length); i++) {
            if (itemName == $item_data_set[i]['item_name'] && batch == $item_data_set[i]['batch_no'] && batch != "" && $item_data_set[i]['deleted'] != 1) {
                $('#item-purchase-modal-editor').modal('toggle');
                alert("Same Item/Batch not allowed");
                return false;
            }
        }
    }
})


$("#expiry").blur(function () {
    expiryValidations();
})

$("#id_nos_free").focus(function () {
    $(this).blur(function () {
        var free_strip = parseInt($("#id_strip_free").val());
        var free_nos = parseInt($("#id_nos_free").val());
        var conv = parseInt($("#id_unit").val());
        var total_qty = free_strip * conv + free_nos;
        if (free_nos / conv >= 1) {
            free_strip = free_strip + Math.floor(free_nos / conv);
            $("#id_strip_free").val(free_strip);
            $("#id_nos_free").val(free_nos % conv);
        }
    })
})

$("#id_strip_free,  #id_nos_free, #id_sales, #id_amount").focus(function () {
    NosConversionStrip();
})

//write amount on its input
$("#id_sales").blur(function () {
    var conv = $("#id_unit").val();
    var strip = $("#id_strip_qty").val();
    var nos = $("#id_nos_qty").val();
    var sales_rate = $("#id_sales").val();
    var free_strip = $("#id_strip_free").val();
    var nos_free = $("#id_nos_free").val();
    var rate = $("#id_purchase").val();
    var disc = parseFloat($("#id_discount").val());

    var trade_rate = parseFloat($("#id_trade_rate").val());
    var inst_rate = parseFloat($("#id_inst_rate").val());
    var std_rate = parseFloat($("#id_std_rate").val());
    var mrp = parseFloat($("#id_mrp").val());

    if (strip == "") $("#id_strip_qty").val(0);
    if (nos == "") $("#id_nos_qty").val(0);
    if (free_strip == "") $("#id_strip_free").val(0);
    if (nos_free == "") $("#id_nos_free").val(0);
    if (sales_rate == "") $("#id_sales").val(0.00);
    if (rate == "") $("#id_purchase").val(0.00);

    rate = parseFloat(rate);
    sales_rate = parseFloat(sales_rate);
    strip = parseFloat(strip);
    nos = parseFloat(nos);

    if (rate == 0) {
        $("#id_purchase").focus();
        alert("Please enter Purchase Price");
        return false;
    }

    if (trade_rate == 0 || trade_rate == "") $("#id_trade_rate").val((rate / 10).toFixed(2));
    if (inst_rate == 0 || inst_rate == "") $("#id_inst_rate").val(sales_rate.toFixed(2));
    if (std_rate == 0 || std_rate == "") $("#id_std_rate").val((sales_rate - sales_rate * (16 / 100)).toFixed(2));
    if (mrp == 0 || mrp == "") $("#id_mrp").val(sales_rate.toFixed(2));
    var amount = rate * (strip + nos / conv);
    $("#id_amount").val(amount.toFixed(2));
})

//Handling Discount and Excise, Other Charges
function adjustAmount() {
    var cgst = parseFloat($("#id_cgst option:selected").val());
    var sgst = parseFloat($("#id_sgst option:selected").val());
    var disc = parseFloat($("#id_discount").val());
    var amount = AdjustAmount();
    amount -= amount * (disc / 100);
    amount = amount + amount * (cgst + sgst) / 100;
    $("#id_amount").val(amount.toFixed(2));
}
$("#id_amount").blur(function () {
    adjustAmount();
})

$("#id_other_charge").focus(function () {
    adjustAmount();
})

$("#id_excise, #id_excise_type").focus(function () {
    var disc = parseFloat($("#id_discount").val());
    var amount = AdjustAmount();
    amount -= amount * (disc / 100);
    $("#id_amount").val(amount.toFixed(2));

})

//change the value of total amount aND net amount

$("#purchase-item-submit").focus(function () {
    adjustAmount();
    $editMode = false;
    $createMode = false;
    $(this).click();
})

$("#id_nos_qty").blur(function () {
    var strip = ($("#id_strip_qty").val());
    var nos = ($("#id_nos_qty").val());
    if (strip == "") {
        ($("#id_strip_qty").val(0));
    }
    if (nos == "") {
        ($("#id_nos_qty").val(0));
    }
    if (strip == 0 && nos == 0) {
        alert("Please Enter Some Qty");
        $("#id_strip_qty").focus();
        return false;
    }
})
$(document).on('keypress', "input:not([readonly], :disabled, .main-btn), select", function (e) {
    if (e.which == 13) {
        e.preventDefault();
        var index = $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").index(this) + 1;
        $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").eq(index).focus();
    }
});
$(document).on('keypress', "input:not([readonly], :disabled, .main-btn, #id_item_id, #id_supplier_id), select", function (e) {
    if (e.shiftKey && e.which == 13) {
        e.preventDefault();
        var index = $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").index(this) - 1;
        $("select:enabled, input:not([readonly], :disabled, .main-btn), input[type='search']").eq(index).focus();
    }
});

$("#id_paid_amount").blur(function () {
    // $(this).blur(function(){
    $("#id_paid_discount").focus();
    // })
})

$("#gif_load_iten_batches").css("display", "block");

$("#id_paid_adj").blur(function () {
    var adj_paid = $(this).val();
    if (adj_paid == "")
        $(this).val(0.00);
    adj_paid = parseFloat($(this).val());
    // var net_adj = parseFloat($("#id_net_adj").val());
    // var net_amount = parseFloat($("#id_net_amount").val());
    // var adj_paid_type = $("#id_paid_adj_type option:selected").text();
    // if(adj_paid_type == "-")    adj_paid = (-1)*adj_paid;
    // if(net_adj != 0)    net_amount = net_amount - net_adj;
    // net_amount = net_amount + net_adj;
    // var net_amount = $("#id_net_amount").val(net_amount.toFixed(2));
    $("#id_net_adj").val(adj_paid);
})

$("#Item-purchase-form").submit(function () {
    $("#item-purchase-modal-editor").modal("hide");
});

$("#id_batch_no").attr("required", true);

$("#search_inv_btn").click(function () {
    var pur_inv = $('#search_inv_input').val();
    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "pur_inv": pur_inv
    };
    $.ajax({
        type: 'GET',
        url: '/purchase/ajax/search_inv',
        data: data,
        beforeSend: function(){
            $("#purchase_inv_search").toggle();
            $(".loading").show();
        },
        complete: function () {
            $(".loading").hide();
        },
        success: function (data) {
            if (parseInt(data['status']) == 1) {
                location.href = data['msg']
            } else {
                $("#purchase_inv_search").toggle();
                $("#search_inv_input").focus();
                $("#seearch_error").css("display", "inline");
            }
        },
        error: function (data) {
            $("#purchase_inv_search").toggle();
            $("#search_inv_input").focus();
            $("#seearch_error").css("display", "inline");
        }
    });
})

$(".modal-wide").on("show.bs.modal", function () {
    var height = $(window).height() - 200;
    $(this).find(".modal-body").css("max-height", height);
});

$("#id_doc_no").attr("readonly", "readonly");



$(document).ready(function () {
    $(".purchase").addClass("active");
    AutoCompleteData("/company/api/supplier-list/?format=json", 'supplierData', "#id_supplier_id", 40, 1);
    LoadAutoCompleteItemData();
    $("#add_supplier, #edit_supplier").click(function () {
        localStorage.removeItem("supplierData"); // remove the localStorage of unitData JSON data
    })
    $(document).on("click", ".edit_row", function () {

        var id_ = $(this).attr("id");
        var data = parseInt($(this).attr("data"));
        $("#id_batch_no").attr("readonly", true);
        $("#id_item_id").attr("readonly", true);
        fillEditValues($item_data_set[data]);
        $("#id_nos_qty").focus();
        $createMode = false;
        $editMode = true;
    })

    $(document).on("click", ".del_row", function () {
        var data_val = parseInt($(this).attr("data"));
        var r = confirm("Do you want to delete item: " + $item_data_set[data_val]['item_name']);
        if (r == true) {
            var deleted_item_amt = parseFloat($item_data_set[data_val]['amount']);
            var total_amt = parseFloat($("#id_net_amount").val()) - deleted_item_amt;
            $("#id_net_amount").val(total_amt.toFixed(2));

            var deleted_item_disc = parseFloat($item_data_set[data_val]['disc_amt']);

            var total_disc_amt = parseFloat($("#id_net_discount").val()) - deleted_item_disc;
            $("#id_net_discount").val(total_disc_amt.toFixed(2));

            var deleted_item_cgst_amt = parseFloat($item_data_set[data_val]['cgst_amt']);
            var total_cgst_amt = parseFloat($("#id_net_cgst").val()) - deleted_item_cgst_amt;
            $("#id_net_cgst").val(total_cgst_amt.toFixed(2));

            var deleted_item_sgst_amt = parseFloat($item_data_set[data_val]['sgst_amt']);
            var total_sgst_amt = parseFloat($("#id_net_sgst").val()) - deleted_item_sgst_amt;
            $("#id_net_sgst").val(total_sgst_amt.toFixed(2));

            //after submit the form remove the null values.
            /*            $item_data_set.splice($.inArray($item_data_set[data_val], $item_data_set),1);*/
            $item_data_set[data_val]['deleted'] = 1;
            var id_ = "item_" + String(data_val);
            $("#" + id_).remove();
        } else {
            return false;
        }
    })
    
    $("#id_item_id").blur(function(){
        if ($("#item_id_field").val() == ""){
            $("#id_batch_no").focus();
            alert("Item not selected. Try again");
            $(this).val("");
        }
    })

    // Submit the Dtl form
    $("#Item-purchase-form").submit(function (event) {
        event.preventDefault();

        if (!SubmitValidation1()) return false;

        var formdata = $(this).serializeArray();
        var data = {};
        $(formdata).each(function (index, obj) {
            data[obj.name] = obj.value;
        });

        data['item_name'] = $("#id_item_id").val();

   
        data['item_id'] = $("#item_id_field").val();

        data['conv'] = $("#id_unit").val();
        data['mrp'] = parseFloat($("#id_sales").val()).toFixed(2);
        data['rate'] = parseFloat($("#id_purchase").val()).toFixed(2);
        data['strip_stock'] = $("#strip_stock").val();
        data['nos_stock'] = $("#nos_stock").val();
        data['batch_no'] = $("#id_batch_no").val();
        data['cgst'] = $("#id_cgst option:selected").val();
        data['sgst'] = $("#id_sgst option:selected").val();
        data['inst_rate'] = $("#id_inst_rate").val();
        data['trade_rate'] = $("#id_trade_rate").val();
        data['std_rate'] = $("#id_std_rate").val();
        data['deleted'] = 0;

        var amt = AdjustAmount();
        var disc_amt = (parseFloat(data['discount']) / 100) * amt;

        data['disc_amt'] = (disc_amt / 1.00).toFixed(2);

        var taxable = data['taxable'] = (amt - disc_amt).toFixed(2);
        var cgst_amt = data['cgst_amt'] = (parseFloat(data['cgst'] / 100) * taxable).toFixed(2);
        var sgst_amt = data['sgst_amt'] = (parseFloat(data['sgst'] / 100) * taxable).toFixed(2);
        var expiry_old = $("#expiry").val();
        if (/(([0-9][0-9])\/([2][0][0-9][0-9]))/.test(expiry_old)) {
            var yr = expiry_old.slice(3, 7);
            var month = expiry_old.slice(0, 2);
            var expiry_new = yr + "-" + month + "-" + daysInMonth(month, yr);
            data['expiry'] = expiry_new;
        }


        if (!HandleEditItem(data)) return false; // Handle Editing in hte Item Table

        $item_data_set.push(data);

        populate_amount(false, 0, parseFloat(data['amount']));
        populate_less_disc(false, 0, parseFloat(disc_amt));
        populate_gst(false, 0, parseFloat(sgst_amt), 0, parseFloat(cgst_amt));

        AddNewRow(data) // Add a new row to Table
        $uid++;
    })
})

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
            url: "/purchase/ajax/delete_inv",
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
});

function checkSuppAndInvDuplicate() {
    var challanNo = $("#id_supp_chal_no").val();
    var supplierName = $("#id_supplier_id").val();
    if (challanNo == "" || supplierName == "")
        return false;
    var data = {
        "challanNo": challanNo,
        "supplierName": supplierName,
        "csrftoken": csrftoken,
    }
    $.ajax({
        type: "POST",
        datatype: 'json',
        contentType: "application/json; charset=utf-8",
        url: "/purchase/ajax/checkSupplieNameInv",
        data: JSON.stringify(data),
        
        success: function (data) {
        },
        error: function () {
            $("#id_supp_chal_no").val("");
            $("#id_supplier_id").val("");
            $("#id_supplier_id").focus();
            alert("Purchase Invoice already exists");

        }
    })
}

function wrapHrdFormValues() {
    var purchase_info = {};
    var key, value;
    $('input, select').each(function () {
        key = $(this).attr("name");
        if (key != "csrfmiddlewaretoken" && key != "initial-supp_chal_dt" && key != "initial-doc_dt") {
            purchase_info[key] = $(this).val();
        }
        if (key == "doc_dt" || key == "supp_chal_dt") {
            var regex = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/;
            var doc_dt = $(this).val();
            if (regex.test(doc_dt)) {
                doc_dt = doc_dt.slice(6, 10) + "-" + doc_dt.slice(0, 2) + "-" + doc_dt.slice(3, 5);
                purchase_info[key] = doc_dt;
            }
        }
        if (key == "net_amount") {
            return false;
        }
    });
    return purchase_info;
}

function saveUpdateMethod(url) {
    $('#save, #update').click(function (e) {
        e.preventDefault();
        var $this = $(this);
        $this.button('loading');

        if ($("#id_supplier_id").val() == "") {
            alert("Supplier name is required\n");
            $("#id_supplier_id").focus();
            $this.button('reset');
            return false;
        }
        if ($("#id_supp_chal_no").val() == "") {
            alert("Supplier Challan no. is required\n");
            $("#id_supp_chal_no").focus();
            $this.button('reset');
            return false;
        }
        var data = {
            "csrfmiddlewaretoken": csrftoken,
            "pur_info": wrapHrdFormValues(),
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
                if (data.status == 1) {
                    window.location = data.url;
                }
            },
            error: function (data) {
                $this.button('reset');
                var error = data.responseJSON;
                $.each(error, function (key, value) {
                    alert(key + " : " + JSON.stringify(value));
                });
            }
        });
    }); //end of save function
    
}
