from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from accounts.models import Accounts, Head, YearEnding
from item_master.models import Item, Batch


class Doctor(models.Model):
	name = 		models.CharField(max_length=80, unique=True, db_index=True)
	code =		models.CharField(max_length = 30, null = True, blank = True)
	add1 = 		models.CharField(max_length = 100, null = True, blank = True)
	add2 = 		models.CharField(max_length = 100, null = True, blank = True)
	add3 = 		models.CharField(max_length = 100, null = True, blank = True)
	contact1 = 	models.CharField(max_length = 12, null = True, blank = True)
	contact2 = 	models.CharField(max_length = 12, null = True, blank = True)
	contact3 = 	models.CharField(max_length = 12, null = True, blank = True)
	discount = 	models.IntegerField(null = True, blank = True, default = 0)

	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.use_date = timezone.now()
		self.use_time = timezone.now()

		return super(Doctor, self).save(*args, **kwargs)


class Party(models.Model):
	name = models.CharField(max_length=80, unique=True, db_index=True)
	person =	models.CharField(max_length = 150, null = True, blank = True)
	add1 = 		models.CharField(max_length = 100, null = True, blank = True)
	add2 = 		models.CharField(max_length = 100, null = True, blank = True)
	add3 = 		models.CharField(max_length = 100, null = True, blank = True)
	city = 		models.CharField(max_length = 30, null = True, blank = True)
	phone1 = 	models.CharField(max_length = 12, null = True, blank = True)
	phone2 = 	models.CharField(max_length = 12, null = True, blank = True)
	user_id = 	models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date =	models.DateField(null = True, blank = True)
	use_time = 	models.TimeField(null = True, blank = True)

	account_id =models.ForeignKey(Accounts, default = 1)
	head_id = 	models.ForeignKey(Head, default = 1)
	less_by = 	models.IntegerField(default = 0, null = True, blank = True)
	identity = 	models.CharField(max_length = 30, null = True, blank = True)

	def __str__(self):
		return self.name


disc_choice = (
		("Rs", "Rs"),
		("Percent", "%"),
)
mode_choices = (
	("CASH", "CASH"),
	("CREDIT", "CREDIT"),
	("BANK", "BANK"),
)
class SalesInvHrd(models.Model):
	doc_no = models.IntegerField(blank=True, null=True, db_index=True)
	doc_dt = 		models.DateField(default = timezone.now)
	message = 		models.CharField(max_length = 300, null = True, blank = True)
	party_id = 		models.ForeignKey(Party, default = 1)

	mode = 			models.CharField(max_length=10, choices = mode_choices, default = "CASH")
	sale_discount = models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	sale_disc_type =models.CharField(max_length=10, choices = disc_choice, default = "Percent")
	sale_adjustment=models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	due_date = 		models.DateField(null = True, blank = True)

	net_amount = 	models.DecimalField(max_digits=10, decimal_places=2, default = 0.00, blank = True)
	rec_amt = 		models.DecimalField(max_digits=10, decimal_places=2, default = 0.00, blank = True)

	net_cgst = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	net_sgst =		models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	net_gst =		models.DecimalField(max_digits=8, decimal_places=2, default = 0.00,  blank = True)

	due_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	doctor_id = 	models.ForeignKey(Doctor, default = 1)

	user_id = 		models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date =		models.DateField(null = True, blank = True)
	use_time = 		models.TimeField(null = True, blank = True)
	ref_note = 		models.CharField(max_length = 50, null = True, blank = True)
	note_value = 	models.IntegerField( blank = True, default = 0)
	token = 		models.IntegerField( blank = True, default = 0)
	opd = 			models.CharField(max_length = 50, null = True, blank = True)

	session_id = models.ForeignKey(YearEnding, default=1, db_index=True)

	class Meta():
		unique_together = ("doc_no", "session_id")

	def __str__(self):
		return str(self.id)

	def get_absolute_edit_url(self):
		return reverse("sales:edit", kwargs={"pk" : self.pk})

	def get_absolute_url(self):
		return reverse("sales:detail", kwargs={"pk" : self.pk})



def post_save_sale_hrd_item(sender, instance, **kwargs):
	post_save.disconnect(post_save_sale_hrd_item, sender=sender)

	instance.use_date = timezone.now()
	instance.use_time = timezone.now()
	instance.save()
	post_save.connect(post_save_sale_hrd_item, sender=sender)

post_save.connect(post_save_sale_hrd_item, sender = SalesInvHrd)



class SalesInvDtl(models.Model):
	sequence = models.AutoField(primary_key=True, db_index=True)
	hrd_id = models.ForeignKey(
		SalesInvHrd, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
	#test models.CASCADE
	item_id = 		models.ForeignKey(Item, db_index = True)
	batch_no = models.CharField(max_length=15, db_index=True)
	strip_qty = 	models.IntegerField( blank =True, default = 0)
	nos_qty = 		models.IntegerField(blank =True, default = 0)
	strip_free = 	models.IntegerField(blank =True, default = 0)
	nos_free = 		models.IntegerField(blank =True, default = 0)
	#scheme_id  linked to SCHEME
	disc_type = 	models.CharField(max_length = 10, choices = disc_choice, default = "Percent")
	discount = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	disc_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	excise_type = 	models.CharField(max_length = 10, choices = disc_choice, default = "Percent")
	excise = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	excise_amt = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	st_rate = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	scharge_rate = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	sgst_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)
	cgst_amt = 		models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	other_charge = 	models.DecimalField(max_digits=6, decimal_places=2, default = 0.00, blank = True)

	amount = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	rate = 			models.DecimalField(max_digits=8, decimal_places=2, default = 0.00, blank = True)
	td = 			models.IntegerField(default = 1, blank = True)

	def __str__(self):
		return self.batch_no

	class Meta():
		unique_together = ("hrd_id", "item_id", "batch_no")

	def get_item_name(self, *args, **kwargs):
		return self.item_id.name

	def get_item_id(self, *args, **kwargs):
		return self.item_id.id

	def get_item_c_s_gst(self, *args, **kwargs):
		return (self.item_id.cgst, self.item_id.sgst)

	def get_batch_instance(self, *args, **kwargs):
		try:
			return Batch.objects.get(batch_no = self.batch_no, item_id = self.item_id)
		except:
			return None

	def get_unit_conv(self, *args, **kwargs):
		return self.item_id.unit_id.number


def post_save_sale_dtl_item(sender, instance, **kwargs):
	post_save.disconnect(post_save_sale_dtl_item, sender=sender)
	if instance.excise:
		if instance.excise_type == "%":
			instance.excise_amt = (instance.amount)*((instance.excise)/100)
		else:
			instance.excise_amt = instance.excise

	if instance.discount:
		if instance.disc_type == "%":
			instance.disc_amt = (instance.amount)*((instance.discount)/100)
		else:
			instance.disc_amt = instance.discount
	instance.save()

	post_save.connect(post_save_sale_dtl_item, sender=sender)

post_save.connect(post_save_sale_dtl_item, sender = SalesInvDtl)
