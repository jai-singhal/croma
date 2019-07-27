from ..models import Chain, Company, Supplier
from rest_framework import serializers

class ChainApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')
	class Meta:
		model = Chain
		fields = [
			"value",
		]


class CompanyApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')

	class Meta:
		model = Company
		fields = [
			"id",
			"value",
		]

class SupplierApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')

	class Meta:
		model = Supplier
		fields = [
			"id",
			"value",
		]
