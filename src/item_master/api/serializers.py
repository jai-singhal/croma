from ..models import Item
from rest_framework import serializers

class ItemApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')
	class Meta:
		model = Item
		fields = [
			"id",
			"value",
		]

