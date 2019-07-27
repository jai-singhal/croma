from django import forms
from .models import *

class SalesInvHrdForm(forms.ModelForm):
	party_id = forms.CharField(max_length = 80, required = True)
	doctor_id = forms.CharField(max_length = 80, required = True)
	class Meta:
		model = SalesInvHrd
		fields = [
			"doc_dt",
			"message",
			"mode",
			"sale_discount",
			"sale_disc_type",
			"sale_adjustment",
			"due_date",
			"rec_amt",
			"net_amount",
			"doctor_id",
			"net_cgst",
			"net_sgst",
			"net_gst",
		]


class SalesInvDtlForm(forms.ModelForm):
	class Meta:
		model = SalesInvDtl
		fields = '__all__'




class DoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = '__all__'
