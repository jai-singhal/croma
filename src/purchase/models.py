from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from accounts.models import Accounts, Head, YearEnding
from item_master.models import Item, Batch
from company_master.models import Supplier


disc_choice = (
		("Percent", "%"),
		# ("Rs", "Rs"),
)
mode_choices = (
	("CASH", "CASH"),
	("CREDIT", "CREDIT"),
	("BANK", "BANK"),
)
oa_type_choice = (
	('Positive', '+'),
	('Nagetive', '-')
)
gst_choice = (
	('0', '0'),
	('2.5', '2.5'),
	('6', '6'),
	('9', '9'),
	('14', '14'),
)

class PurchaseInvHrd(models.Model):
    
	doc_no = 		models.IntegerField(blank = True, null = True, db_index=True)
	doc_dt = 		models.DateField(default = timezone.now)
	supplier_id = 	models.ForeignKey(Supplier, default = 1)
	p_method = 		models.CharField(max_length = 50, choices = mode_choices, default = "CASH") #link to
	supp_chal_no = 	models.CharField(max_length = 50, null = True, blank = True, db_index=True) #link to
	supp_chal_dt =	models.DateField(default = timezone.now)

#Fields generated according item added
	net_discount = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	net_cgst = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	net_sgst = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	net_adj = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	net_amount = 	models.DecimalField(max_digits=10, decimal_places=2, default = 0.00) #item amount

#filed that are defined by purchase bill
	paid_discount = models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	paid_cgst = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	paid_sgst = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	paid_adj = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	paid_adj_type = models.CharField(max_length = 10, choices = oa_type_choice, default = 'Positive')
	paid_amount = 	models.DecimalField(max_digits=10, decimal_places=2, default = 0.00, blank = True)

	user_id = 		models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date =		models.DateField(null = True, blank = True)
	use_time = 		models.TimeField(null = True, blank = True)
	due_amt = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	ref_note = 		models.CharField(max_length = 80, blank = True, null = True) #link to
	session_id = models.ForeignKey(YearEnding, default=1, db_index=True)

	def __str__(self):
		return str(self.doc_no)

	def get_absolute_edit_url(self):
		return reverse("purchase:edit", kwargs={"pk" : self.pk})

	def get_absolute_url(self):
		return reverse("purchase:detail", kwargs={"pk" : self.pk})
	# method for updating
	class Meta:
		unique_together = (
			("session_id", "doc_no"), 
			("supplier_id", "supp_chal_no", "session_id")
		)


class PurchaseInvDtl(models.Model):
	hrd_id = 		models.ForeignKey(PurchaseInvHrd, on_delete=models.CASCADE, null = True, blank = True, db_index = True)
	item_id = 		models.ForeignKey(Item, db_index = True)
	batch_no = 		models.CharField(max_length = 15, db_index = True)
	strip_qty = 	models.IntegerField(blank =True, default = 0)
	nos_qty = 		models.IntegerField(blank =True, default = 0)
	strip_free = 	models.IntegerField(blank =True, default = 0)
	nos_free = 		models.IntegerField(blank =True, default = 0)
	#scheme_id  linked to SCHEME
	disc_type = 	models.CharField(max_length = 10, choices = disc_choice, default = "Percent")
	discount = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0, blank = True)
	disc_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	excise_type = 	models.CharField(max_length = 10, choices = disc_choice, default = "Percent")
	excise = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	excise_amt = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	st_rate = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0, blank = True)
	other_charge = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	cgst = 			models.CharField(max_length = 3, choices = gst_choice, default = '6')
	sgst = 			models.CharField(max_length = 3, choices = gst_choice, default = '6')
	sgst_type = 	models.CharField(choices = disc_choice, default='Percent', max_length=10)
	cgst_type = 	models.CharField(choices = disc_choice, default='Percent', max_length=10)

	sgst_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0, blank = True)
	cgst_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	scharge_rate = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	amount = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	rate = 			models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	td = 			models.IntegerField(default = 1, null = True, blank = True)

	class Meta():
		unique_together = ("hrd_id", "item_id", "batch_no")

	def __str__(self):
		return str(self.id)

	def get_item_name(self, *args, **kwargs):
		return self.item_id.name

	def get_item_id(self, *args, **kwargs):
		return self.item_id.id

	def get_item_gst(self, *args, **kwargs):
		return (self.item_id.cgst, self.item_id.sgst)

	def get_batch_instance(self, *args, **kwargs):
		try:
			return Batch.objects.get(item_id = self.item_id, batch_no = self.batch_no)
		except:
			return None

	def get_unit_conv(self, *args, **kwargs):
		return self.item_id.unit_id.number
