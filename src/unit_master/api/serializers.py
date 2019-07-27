from ..models import Unit
from rest_framework import serializers

class UnitApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')

	class Meta:
		model = Unit
		fields = [
			"id",
			"value",

		]
