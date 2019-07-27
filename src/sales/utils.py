def create_SaleInvDtl_JSON_QuerySet(saleInvDtl_queryset):
	sale_dtl_item_arr = []
	for item in saleInvDtl_queryset:
		item_set = {}
		batch_instance = item.get_batch_instance()

		item_set['item_id'] = str(item.get_item_id())
		item_set['item_name'] = str(item.get_item_name())
		item_set['batch_no'] = 	str(item.batch_no)

		item_set['strip_qty'] = int(item.strip_qty)
		item_set['nos_qty'] = 	int(item.nos_qty)
		item_set['strip_free'] = 	int(item.strip_free)
		item_set['nos_free'] = 	int(item.nos_free)
		item_set['mrp'] = 		float(item.rate)
		item_set['rate'] = 		float(item.rate)

		item_set['amount'] = 	float(item.amount)
		item_set['discount'] = 	float(item.discount)
		item_set['disc_type'] = str(item.disc_type)
		item_set['excise'] = 	float(item.excise)
		item_set['excise_type'] = str(item.excise_type)
		item_set['other_charge'] = float(item.other_charge)
		item_set['conv'] = float(item.get_unit_conv())

		gst = item.get_item_c_s_gst()
		item_set['cgst'] = gst[0]
		item_set['sgst'] = gst[1]
		item_set['sgst_amt'] = 	float(item.sgst_amt)
		item_set['cgst_amt'] = 	float(item.cgst_amt)

		try:
			strip_stock, nos_stock = batch_instance.strip, batch_instance.nos
			item_set['pur_rate'] =	 float(batch_instance.strip_pur)
			item_set['expiry'] = 	str(batch_instance.expiry.strftime("%Y-%m"))
		except:
			strip_stock, nos_stock = 0, 0
			item_set['pur_rate'] = 0.00
			item_set['expiry'] = "-"

		item_set['strip_stock'] = int(strip_stock)
		item_set['nos_stock'] = int(nos_stock)

		item_set['deleted'] = 0;
		sale_dtl_item_arr.append(item_set)

	return sale_dtl_item_arr
