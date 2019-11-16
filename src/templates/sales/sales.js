var $uid = 0;
var $item_data_set;

{% if not is_retrieve %}
$(document).unbind("keyup").keyup(function(e){
	if (e.which == 118) {
		$("#search_item_modal").modal("show");
	}
	if(e.which == 120) {
		$("#item-sale-modal-editor").modal("show");
		$("#Item-sale-form").trigger("reset");
		$("#id_batch_no").attr("readonly", false);
		$("#id_item_id").attr("readonly", false);
		$('#id_item_id').focus();
		$createMode = true;
		$editMode = false;
	}
});
$(document).ready(function(){
	AutoCompleteData("/sales/api/doctor-list/?format=json", 'doctorData', "#id_doctor_id", 15, 1);
	AutoCompleteData("/sales/api/party-list/?format=json", 'patientData', "#id_party_id", 10, 1);
	LoadAutoCompleteItemData();
})
{% endif %}

$(document).ready(function() {
	{% if is_create %}
	$("#id_party_id").focus();

	$("#id_doc_dt").removeAttr("type");
	$("#id_doc_dt").datepicker();
	{% endif %}

	{% if is_retrieve %}
	$("select").attr("disabled", true);
	$("#search_inv_input").attr("readonly", false);
	$("#search_inv_input").focus(function(){
		$("#seearch_error").css("display", "none");
	});
	$(document).unbind("keyup").keyup(function(e){
		if(e.which == 120) {
			alert("You cannot create/edit item in this Mode");
		}
	});
	{% endif %}
	{% if is_update %}
	$("#id_party_id").focus();
	$("#id_doc_dt").removeAttr("type");
	$("#id_doc_dt").datepicker();
	{% endif %}

	{% if is_create %}
        $item_data_set = []; //array to store the itmes
        {% else %}
        $item_data_set = JSON.parse('{{saleDtl_item_set_json | escapejs}}');
        fill_item_table($item_data_set);
        $uid = $item_data_set.length;
        {% endif %}

        var url;
        {% if is_update %}
        url = "{{instance.get_absolute_edit_url}}";
        {% else %}
        url = "/sales/create/";
        {% endif %}
        saveUpdateMethod(url);

}) //end of document ready function


