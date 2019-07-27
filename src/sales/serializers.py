from rest_framework.serializers import  ModelSerializer
from .models import *
       
class SalesInvHdrSerialzer(ModelSerializer):
	class Meta:
		model = SalesInvHrd
		fields = '__all__'

	def __init__(self, instance=None, data=None, *args, **kwargs):
		party_qs = Party.objects.filter(name=data['party_id'])
		if party_qs.exists():
			data['party_id'] = party_qs.first().id
		else:
			newObj = Party.objects.create(name=data['party_id'])
			data['party_id'] = newObj.id

		doc_qs = Doctor.objects.filter(name=data['doctor_id'])
		if doc_qs.exists():
			data['doctor_id'] = doc_qs.first().id
		else:
			data['doctor_id'] = 0

		super(SalesInvHdrSerialzer, self).__init__(instance, data, *args, **kwargs)


class SalesInvDtlSerialzer(ModelSerializer):
	class Meta:
		model = SalesInvDtl
		fields = '__all__'






