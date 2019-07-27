from django import forms
from accounts.models import YearEnding
import calendar
from item_master.models import Item
from company_master.models import Supplier
from django.contrib.admin.widgets import AdminDateWidget

class InvoiceStatementForm(forms.Form):
	from_dt = forms.DateField(widget = AdminDateWidget)
	to_dt = forms.DateField(widget = AdminDateWidget)
	
	def __init__(self, *args, **kwargs):
		session_id = kwargs.pop('session_id')
		obj = YearEnding.objects.get(id = session_id)
		from_dt = obj.from_dt
		to_dt = obj.to_dt
		self.Year_Choices = [from_dt.year, to_dt.year]
		super(InvoiceStatementForm, self).__init__(*args, **kwargs)


class ItemWiseReportForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(ItemWiseReportForm, self).__init__(*args, **kwargs)

	from_dt = forms.DateField()
	to_dt = forms.DateField()
	item = forms.CharField()

	def clean(self):
		cleaned_data = super(ItemWiseReportForm, self).clean()
		item = cleaned_data.get("item")

		if not Item.objects.filter(name = item).exists():
		    raise forms.ValidationError(
		    	"Item Does Not Exists"
		    )

class ItemSupplierWiseReportForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(ItemSupplierWiseReportForm, self).__init__(*args, **kwargs)

	from_dt = forms.DateField()
	to_dt = forms.DateField()
	item = forms.CharField()
	supplier = forms.CharField()

	def clean(self, *args, **keyargs):
		item = self.cleaned_data.get("item")
		supplier = self.cleaned_data.get("supplier")
		print(item, supplier)
		if not Item.objects.filter(name = item).exists():
			print(item, supplier)
			raise forms.ValidationError("Item Does Not Exists" )

		if not Supplier.objects.filter(name = supplier).exists():
		    raise forms.ValidationError("Supplier Does Not Exists")


class ExpiryReport(forms.Form):
	expiry = forms.DateField()
	exp_upto_mon = forms.BooleanField()
	exp_of_mon = forms.BooleanField()


class InventoryReport(forms.Form):
	name = forms.CharField()

