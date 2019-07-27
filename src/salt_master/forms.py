from django import forms
from .models import Salt


class SaltForm(forms.ModelForm):
	class Meta:
		model = Salt
		fields = [
			"name",
		]