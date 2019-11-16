function makeclass_item_batch(item_name) {
    var text = item_name;
    var possible = "abcdefghijklmnopqrstuvwxyz";
    for (var i = 0; i < 2; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function ItemOnSelect(suggestion) {
    if ($("#id_item_id").attr("readonly"))
        return false;

    var data = {
        "csrfmiddlewaretoken": csrftoken,
        "item_id": suggestion.id
    };
    $.ajax({
        type: 'GET',
        url: '/item/ajax/get/item_batches',
        data: data,

        beforeSend: function () {
            $("#gif_load_item_batches").css("display", "block");
            $(".loading").show();
        },
        complete: function () {
            $(".loading").hide();
        },
        success: function (data) {
            ItemOnSelectAjaxSuccess(data);
            $("#gif_load_item_batches").css("display", "none");

        },
        error: function (data) {
            alert("Something went wrong in Batch Item");
        }
    });
}

function ItemOnSelectAjaxSuccess(data) {
    var batch_data = JSON.parse(data['batch_query']);
    var item_data = JSON.parse(data['instance']);
    $("#item_id_info").html(item_data['item_code']);
    $("#item_company_info").html(item_data['company']);
    $("#item_salt_info").html(item_data['salt']);
    $("#item_unit_info").html(item_data['unit']);
    $("#item_strip_info").html(item_data['strip_stock']);
    $("#item_nos_info").html(item_data['nos_stock']);
    $("#id_unit").val(item_data['unit_conv']);
    $("#id_cgst").val(item_data['cgst']);
    $("#id_sgst").val(item_data['sgst']);

    var total_batches = batch_data.length;
    if (total_batches == 0) {
        $("#id_batch_no").focus();
    }
    if (total_batches > 0) {

        $('#item_batch_body').animate({
            scrollTop: '=0px'
        });

        //getting the data from ajax call of all batches assoiated with item
        var html_text = "";
        var item_name = String($("#id_item_id").val());

        var get_item_class_name = makeclass_item_batch(item_name.split(" ", "-")[0]);

        // if batch is empty thhen only show the batch table modal
        $("#item_batch_table_modal").addClass(get_item_class_name);
        $("#item_batch_body").addClass(get_item_class_name + "_body");
        $("#item_batch_table_modal").modal('show');


        $(batch_data).each(function (index, element) {
            var class_name = get_item_class_name + "_" + String(index);
            html_text += "<tr class = \'" + class_name + "\'><td>" + element['batch_no'] + "</td> <td>" + element['expiry'] + "</td> <td>" + element['strip'] + "</td> <td>" + element['nos'] + "</td> <td>" + element['strip_sale'] + "</td> <td>" + element['strip_pur'] + "</td> <td>" + element['mrp'] + "</td></tr>"
        });

        $("#batches_content").html(html_text);

        //handling the batch table
        var tr_id = 0;
        var current_row_selector = $("." + get_item_class_name + "_" + String(tr_id));
        current_row_selector.focus();
        current_row_selector.css("background-color", "#6699FF");

        $("." + get_item_class_name).keydown(function (e) {

            if (e.keyCode === 27) { // esc
                $('#item_batch_table_modal').modal('hide');
                $("#id_batch_no").focus();
            }

            if (e.keyCode == 13) {
                $("#id_batch_no").attr("readonly", true);
                $("#id_item_id").attr("readonly", true);

                $('#item_batch_table_modal').modal('hide');
                var selected_batch = batch_data[tr_id];
                // console.log(selected_batch, "selected_batch");
                $("#strip_stock").val(selected_batch['strip']);
                $("#nos_stock").val(selected_batch['nos']);
                $("#id_batch_no").val(selected_batch['batch_no']);
                var expiry = selected_batch['expiry'];
                expiry = expiry.slice(5, 7) + "/" + expiry.slice(0, 4);
                $("#expiry").val(expiry);
                $("#id_purchase").val(selected_batch['strip_pur']);
                $("#id_sales").val(selected_batch['strip_sale']);
                $("#id_mrp").val(selected_batch['mrp']);
                $("#id_inst_rate").val(selected_batch['inst_rt']);
                $("#id_trade_rate").val(selected_batch['trade_rt']);
                $("#id_std_rate").val(selected_batch['std_rt']);

                $("#item_batch_body").removeClass(get_item_class_name + "_body");
                $("#id_nos_qty").focus();
                return false;
            }
            if (e.keyCode == 38 && tr_id > 0) {
                current_row_selector.css("background-color", "white");

                tr_id -= 1;

                $('.' + get_item_class_name + "_body").animate({
                    scrollTop: '-=25px'
                }, 1);
                current_row_selector = $("." + get_item_class_name + "_" + String(tr_id));
                current_row_selector.focus();
                current_row_selector.css("background-color", "#6699FF");

                return false;
            }
            if (e.keyCode == 40 && tr_id < total_batches - 1) {
                current_row_selector.css("background-color", "white");

                tr_id += 1;
                $('.' + get_item_class_name + "_body").animate({
                    scrollTop: '+=25px'
                }, 1);
                current_row_selector = $("." + get_item_class_name + "_" + String(tr_id));
                current_row_selector.focus();
                current_row_selector.css("background-color", "#6699FF");

                return false;
            }
        });
    } //end of if
    else if (total_batches == 0) {
        //IF NO BATCH FOUND FOR ITEM
        $("#id_batch_no").focus();
        $("#nos_stock").val(0);
        $("#strip_stock").val(0);
        return false;
    }
}