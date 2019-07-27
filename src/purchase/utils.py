
def create_PurchaseInvDtl_JSON_QuerySet(PurInvDtl_queryset):
	sale_dtl_item_arr = []
	for item in PurInvDtl_queryset:
		item_set = {}
		batch_instance = item.get_batch_instance()

		item_set['item_name'] = str(item.get_item_name())
		item_set['item_id'] = str(item.get_item_id())
		item_set['batch_no'] = 	str(item.batch_no)
		try:
			item_set['expiry'] = 	str(batch_instance.expiry.strftime("%Y-%m"))
		except:
			item_set['expiry'] = "-"
		item_set['strip_qty'] = int(item.strip_qty)
		item_set['nos_qty'] = 	int(item.nos_qty)
		item_set['strip_free'] = 	int(item.strip_free)
		item_set['nos_free'] = 	int(item.nos_free)
		item_set['rate'] = 		float(item.rate)
		try:
			item_set['mrp'] = 	float(batch_instance.mrp)
		except:
			item_set['mrp'] = 0.00
		try:
			item_set['pur_rate'] =	 float(batch_instance.strip_pur)
		except:
			item_set['pur_rate'] = 0.00
		item_set['amount'] = 	float(item.amount)
		item_set['discount'] = 	float(item.discount)
		item_set['disc_amt'] = 	float(item.disc_amt)

		item_set['disc_type'] = str(item.disc_type)
		item_set['excise'] = 	float(item.excise)
		item_set['excise_type'] = str(item.excise_type)
		item_set['other_charge'] = float(item.other_charge)
		item_set['conv'] = float(item.get_unit_conv())

		item_set['sgst_amt'] = 	float(item.sgst_amt)
		item_set['cgst_amt'] = 	float(item.cgst_amt)

		gst = item.get_item_gst()
		item_set['sgst'] = 	float(gst[1])
		item_set['cgst'] = 	float(gst[0])
		try:
			item_set['trade_rate'] = float(batch_instance.trade_rt)
			item_set['std_rate'] = float(batch_instance.std_rt)
			item_set['inst_rate'] = float(batch_instance.inst_rt)
			item_set['strip_stock'] = int(batch_instance.strip)
			item_set['nos_stock'] = int(batch_instance.nos)
		except:
			item_set['trade_rate'] = 0.00
			item_set['std_rate'] = 0.00
			item_set['inst_rate'] = 0.00
			item_set['strip_stock'] = 0
			item_set['nos_stock'] = 0

		item_set['deleted'] = 0
		sale_dtl_item_arr.append(item_set)

	return sale_dtl_item_arr
