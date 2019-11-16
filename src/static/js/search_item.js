 $("#id_searchmodal_item_id").focus(function () {
     $(".search_item_name").removeClass("has-error");
 })
 $("#item_search").click(function (e) {
     e.preventDefault();
     $("#modal_item_data").html("");
     var item = $("#id_searchmodal_item_id").val();
     data = {
         "item_name": item,
         "csrf_token": csrftoken
     };
     $(".loading").show();
     $.ajax({
         dataType: "json",
         data: data,
         url: '/item/ajax/search/item_info',
         method: "GET",
         complete: function () {
             $(".loading").hide();
         },

         success: function (data) {
             if (data['status'] == "0") {
                 $(".search_item_name").addClass("has-error");
                 return false;
             }
             $(".search_item_name").removeClass("has-error");
             var supplier = data['supplier'];
             var batches = JSON.parse(data['batches']);
             var table = "<div class = 'table-container'><table class = 'table table-hover table-responsive table-bordered'>\
                <thead><tr>\
                <th>Batch</th>\
                <th>Expiry</th>\
                <th>Strip</th>\
                <th>Nos</th>\
                <th>Pur_rt</th>\
                <th>MRP</th>\
                </tr></thead><tbody>"
             for (var i = 0; i < batches.length; i++) {
                 var batch = batches[i]['fields'];
                 table += "<tr>\
                        <td>" + batch['batch_no'] + "</td>\
                        <td>" + batch['expiry'] + "</td>\
                        <td>" + batch['strip'] + "</td>\
                        <td>" + batch['nos'] + "</td>\
                        <td>" + batch['strip_pur'] + "</td>\
                        <td>" + batch['mrp'] + "</td></tr>"
             }
             table += "</tbody></table></div>"
             var data = "<div class='list-group'>\
                                        <li class='list-group-item'><div class = 'row'><div class = 'col-sm-6'>Company: " + data['company'] + "</div><div class = 'col-sm-6'>Supplier: " + supplier + "</div></div></li>\
                                        <li class='list-group-item'>Salt: " + data['salt'] + "</li>\
                                        <li class='list-group-item'><div class = 'row'><div class = 'col-sm-6'>Unit: " + data['unit'] + "</div><div class = 'col-sm-6'>Strip/Nos Stock: " + data['strip_stock'] + "/" + data['nos_stock'] + "</div></div></li>\
                                    </div>"
             $("#modal_item_data").append(data);
             $("#modal_item_data").append(table);
         },
     });
 })
 $(document).ready(function () {
     $('#search_item_modal').on('shown.bs.modal', function () {
         $('#id_searchmodal_item_id').focus();
         LoadAutoCompleteItemData('#id_searchmodal_item_id');
     });
     $("#id_searchmodal_item_id").click(function () {
         $("#modal_item_data").html("");
     })
     $('#id_searchmodal_item_id').focus(function () {
         $(document).unbind("keyup").keyup(function (e) {
             if (e.which == 13) {
                 $("#item_search").click();
             }
         });
     });
 })