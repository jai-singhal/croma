from ..models import Party, Doctor
from rest_framework import serializers

class PartyApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')

	class Meta:
		model = Party
		fields = [
			"id",
			"value",

		]

class DoctorApiSerialzer(serializers.ModelSerializer):
	value = serializers.CharField(source='name')

	class Meta:
		model = Doctor
		fields = [
			"id",
			"value",

		]
