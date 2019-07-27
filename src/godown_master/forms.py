from django import forms
from .models import Godown

class GodownForm(forms.ModelForm):
	class Meta:
		model = Godown
		fields = [
			"name",
		]
