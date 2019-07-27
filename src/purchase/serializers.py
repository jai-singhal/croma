from rest_framework.serializers import  ModelSerializer
from .models import PurchaseInvHrd, PurchaseInvDtl, Supplier

       
class PurchaseInvHdrSerialzer(ModelSerializer):
	class Meta:
		model = PurchaseInvHrd
		fields = '__all__'

	def __init__(self, instance=None, data=None, *args, **kwargs):
		sup_qs = Supplier.objects.filter(name=data['supplier_id'])
		if sup_qs.exists():
			data['supplier_id'] = sup_qs.first().id
		else:
			data['supplier_id'] = 0
		super(PurchaseInvHdrSerialzer, self).__init__(
			instance, data, *args, **kwargs)


class PurchaseInvDtlSerialzer(ModelSerializer):
	class Meta:
		model = PurchaseInvDtl
		fields = '__all__'






