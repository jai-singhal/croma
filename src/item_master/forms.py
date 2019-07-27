from django import forms
from .models import *
from company_master.models import Chain
from salt_master.models import Salt

class ItemMasterForm(forms.ModelForm):
	
	group_id = forms.CharField(max_length = 150, required = True, initial = "AVENTIS PASTEUR")
	salt_id = forms.CharField(max_length = 250, required = True, initial = "TELMISARTAN")
	unit_id = forms.CharField(max_length = 30, required = True, initial = "1*10")

	class Meta:
		model = Item
		fields = "__all__"

class BatchForm(forms.ModelForm):
	class Meta:
		model = Batch
		fields = "__all__"
