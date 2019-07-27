from django import forms
from .models import *


class PurchaseInvHrdForm(forms.ModelForm):
	supplier_id = forms.CharField(max_length = 80, required = True)
	class Meta:
		model = PurchaseInvHrd
		fields = '__all__'

class PurchaseInvDtlForm(forms.ModelForm):
	class Meta:
		model = PurchaseInvDtl
		fields = '__all__'

