from django.forms import ModelForm
from .models import Company, Chain, Supplier


class CompanyForm(ModelForm):
	class Meta:
		model = Company
		fields = [
			"name",
			"short_name",
			"add1",
			"add2",
			"add3",
			"city",
			"phone1",
			"phone2",
			"godown_id",
			"ptax",
			"name",
			"stax",
			"supp_id",
		]

class ChainForm(ModelForm):
	class Meta:
		model = Chain
		fields = [
			"name",
			"master",
			"group",
			"full_path",
			"category",
			"total",
		]

class SupplierForm(ModelForm):
	class Meta:
		model = Supplier
		fields = "__all__"
		exclude = [		
					"user_id", 
					"head_id", 
					"account_id", 
					"use_date", 
					"use_time", 
					"c_limit", 
					"c_days",
					"identity"
				]
