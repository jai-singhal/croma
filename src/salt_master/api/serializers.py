from ..models import Salt
from rest_framework import serializers


class SaltApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')
	class Meta:
		model = Salt
		fields = [
			"id",
			"value",
		]


