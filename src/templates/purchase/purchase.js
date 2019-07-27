var $uid = 0;
var $item_data_set;
var url;

//after submit the form remove the null values.
{% if not is_retrieve %}
$("#id_supp_chal_no").blur(function () {
    checkSuppAndInvDuplicate();
});
$(document).unbind("keyup").keyup(function(e){
    e.preventDefault();
    if (e.which == 118) {
        $("#search_item_modal").modal("show");
    }
    if(e.which == 120) {
        $("#item-purchase-modal-editor").modal("toggle");
        $("#Item-purchase-form").trigger("reset");
        $("#id_batch_no").attr("readonly", false);
        $("#id_item_id").attr("readonly", false);
        $('#id_item_id').focus();
        $createMode = true;
        $editMode = false;
    }
});
{% else %}
    $(document).unbind("keyup").keyup(function(e){
    if(e.which == 120)  alert("You cannot create/edit item in this Mode");

    });
{% endif %}

$(document).ready(function() {
    {% if is_create %}
    $item_data_set = []; //array to store the itmes
    {% else %}
    $item_data_set = JSON.parse('{{saleDtl_item_set_json | escapejs}}');
    fill_item_table($item_data_set);
    $uid = $item_data_set.length;
    {% endif %}

    $("#id_supplier_id").attr("value", "{{instance.supplier_id.name}}");
    {% if is_create %}
        $("#id_supplier_id").focus();

        $("#id_doc_dt").removeAttr("type");
        $("#id_doc_dt").datepicker();
        $("#id_supp_chal_dt").datepicker();
    {% endif %}

    {% if is_retrieve %}
        $("select").attr("disabled", true);
       
        $("#search_inv_input").attr("readonly", false);
        $("#search").click(function(){
            $("#purchase_inv_search").modal("show");
            $("#search_inv_input").focus();
            $("#search_inv_input").val("");
             $("#search_error").css("display", "none");
        })

        $("#search_inv_input").focus(function(){
            $(document).on('keypress', "#search_inv_input", function (e) {
                if (e.which == 13) {
                    e.preventDefault();
                    $("#search_inv_btn").click();
                }
            })
        });
        $("#search_inv_input").focus(function(){
            $("#seearch_error").css("display", "none");
        });
    {% endif %}
    {% if is_update %}
        $("#id_supplier_id").focus();
        $("#id_doc_dt").removeAttr("type");
        $("#id_doc_dt").datepicker();
        $("#id_supp_chal_dt").datepicker();

    {% endif %}

    {% if is_update %}
    url = "{{purchase_query.get_absolute_edit_url}}";
    {% else %}
    url = "/purchase/create/";
    {% endif %}
    saveUpdateMethod(url);
}) //end of document ready function
