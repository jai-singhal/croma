from rest_framework import serializers  
from .models import Batch, Item
from salt_master.models import Salt
from unit_master.models import Unit
from company_master.models import Chain


class ItemSerialzer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = [
			"name",
			"unit_id",
			"item_code",
			'bin_no',
			'group_id',
			"salt_id",
			"stax_id",
			'ptax_id',
			'godown_id',
			"slow_days",
			"min_qty",
			"max_qty",
			"is_active",
			"re_level",
			"re_qty",
			"app",
			"strip_stock",
			"nos_stock",
            'cgst',
            'sgst'
		]

	def __init__(self, instance = None, data = None, *args, **kwargs):
		unit_qs = Unit.objects.filter(name = data['unit_id'])
		if unit_qs.exists():
			data['unit_id'] = unit_qs.first().id
		else:
			data['unit_id'] = 'None'

		group_qs = Chain.objects.filter(name = data['group_id'])
		if group_qs.exists():
			data['group_id'] = group_qs.first().id
		else:
			data['group_id'] = 'None'

		salt_qs = Salt.objects.filter(name = data['salt_id'])
		if salt_qs.exists():
			data['salt_id'] = salt_qs.first().id
		else:
			data['salt_id'] = 'None'

		super(ItemSerialzer, self).__init__(instance, data, *args, **kwargs)

	def validate(self, data):
		qs = Unit.objects.filter(name = data['unit_id'])
		if not qs.exists():
			raise serializers.ValidationError("Error in resolving the Unit name")
		
		return data

	def update(self, instance, validated_data, *args, **kwargs):
		super(ItemSerialzer, self).update(instance, validated_data, *args, **kwargs)
		return instance

class BatchSerialzer(serializers.ModelSerializer):
	class Meta:
		model = Batch
		fields = [
			"id",
			"item_id",
			"batch_no",
			"expiry",
			'strip',
			"nos",
			"strip_pur",
			"strip_sale",
			'mrp',
			"pur_rt",
			"sale_rt",
			"inst_rt",
			"trade_rt",
			"std_rt",
		]

	def __init__(self, instance = None, data = None, item_id = None, *args, **kwargs):
		if type(data) == list:
			for batch in data:
				batch['item_id'] = item_id
		else:
			data['item_id'] = item_id
		super(BatchSerialzer, self).__init__(instance, data, *args, **kwargs)
		