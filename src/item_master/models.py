from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify
from .utils import random_string
from django.core.urlresolvers import reverse
from unit_master.models import Unit
from company_master.models import Company, Chain, Supplier
from salt_master.models import Salt
from godown_master.models import Godown

gst_choice = (
	('0', '0'),
	('2.5', '2.5'),
	('6', '6'),
	('9', '9'),
	('14', '14'),
)

class TaxType(models.Model):
	name = 		models.CharField(max_length = 50, unique = True)
	desc = 		models.CharField(max_length = 50)
	applicable_choices = (
		('Sale', 'Sale'),
		('Purchase', 'Purchase')
	)
	applicable = models.CharField(max_length = 10,
									choices = applicable_choices,
								)
	cst_rt = 		models.DecimalField(max_digits=5, decimal_places=2, default = 0)
	lst_rt =		models.DecimalField(max_digits=5, decimal_places=2, default = 0)
	surcharge_rt =	models.IntegerField(default = 0)
	add_sur =		models.IntegerField(default = 0)
	ac = 			models.CharField(max_length = 50, null = True, blank = True)
	tax_ac = 		models.CharField(max_length = 50, null = True, blank = True)
	calc_on = 		models.CharField(max_length = 50, default = "AFTER DISCOUNT")
	user_id = 		models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date =		models.DateField(null = True, blank = True)
	use_time = 		models.TimeField(null = True, blank = True)

	class Meta:
	    verbose_name = 'TaxType'
	    verbose_name_plural = 'TaxTypes'
	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(TaxType, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

def create_item_code():
   while(True):
      rand_3string = random_string()
      for rand_str in rand_3string:
         if not Item.objects.filter(item_code = rand_str).exists():
            return rand_str

class Item(models.Model):
	item_code = 	models.CharField(max_length = 20, null = True, blank =True)
	name = 			models.CharField(max_length=80, unique=True, db_index=True)
	group_id = 		models.ForeignKey(Chain, default = 37)
	unit_id = 		models.ForeignKey(Unit, default = 601)
	salt_id = 		models.ForeignKey(Salt, default=715)
	godown_id = 	models.ForeignKey(Godown, default=1)
	stax_id = 		models.ForeignKey(TaxType, default=1, related_name = 'ServiceTax', limit_choices_to={'applicable': 'Sale'})
	ptax_id = 		models.ForeignKey(TaxType, default=2, related_name = 'PurchaseTax', limit_choices_to={'applicable': 'Purchase'})

	min_qty = 		models.DecimalField(max_digits=8, decimal_places=2, default = 10, null = True, blank = True)
	max_qty = 		models.DecimalField(max_digits=8, decimal_places=2, default = 20, null = True, blank = True)

	re_level = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0, null = True, blank = True)
	re_qty = 		models.DecimalField(max_digits=8, decimal_places=2, default = 0, null = True, blank = True)

	nac = 			models.IntegerField(null = True, blank = True, default = 0)   #Redundant field (0)
	slow_days = 	models.IntegerField(null = True, blank = True, default = 0) #Redundant field (0)

	is_active = 	models.BooleanField(default = True)

	strip_stock = 	models.IntegerField(default = 0, null = True, blank = True)
	nos_stock = 	models.IntegerField(default = 0, null = True, blank = True)

	user_id = 		models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

	bin_no = 		models.CharField(max_length = 10, null = True, blank = True)
	company_id = 	models.ForeignKey(Company, default = 1)

	sgst = 			models.CharField(default = '6', choices = gst_choice, max_length = 3)
	cgst = 			models.CharField(default = '6', choices = gst_choice, max_length = 3)

	use_date =		models.DateField(null = True, blank = True)
	use_time = 		models.TimeField(null = True, blank = True)
	app = 			models.BooleanField(default = False)

	class Meta:
	    verbose_name = 'Item'
	    verbose_name_plural = 'Items'

	def __str__(self):
		return self.name

	# Subtracting the qty [nos and strip] from Item Table

	def handle_ItemQty_Stock_OnAdd(self, strip, nos, *args, **kwargs):

		total_qty_old = (self.strip_stock)*(self.unit_id.number) + self.nos_stock
		total_qty_new = total_qty_old + strip*(self.unit_id.number) + nos

		if total_qty_new > 0:
			self.strip_stock = (total_qty_new)//(self.unit_id.number)
			self.nos_stock = (total_qty_new)%(self.unit_id.number)
		else:
			total_qty_new = abs(total_qty_new)
			self.strip_stock = (-1)*((total_qty_new)//(self.unit_id.number))
			self.nos_stock = (-1)*((total_qty_new)%(self.unit_id.number))
		self.save()

	def handle_ItemQty_Stock_OnSub(self, strip, nos, *args, **kwargs):

		total_qty_old = (self.strip_stock)*(self.unit_id.number) + self.nos_stock
		total_qty_new = total_qty_old - strip*(self.unit_id.number) - nos
		if total_qty_new > 0:
			self.strip_stock = (total_qty_new)//(self.unit_id.number)
			self.nos_stock = (total_qty_new)%(self.unit_id.number)
		else:
			total_qty_new = abs(total_qty_new)
			self.strip_stock = (-1)*((total_qty_new)//(self.unit_id.number))
			self.nos_stock = (-1)*((total_qty_new)%(self.unit_id.number))

		self.save()

	def handle_c_s_gst(self, cgst, sgst, *args, **kwargs):
		if self.cgst != cgst or self.sgst != sgst:
			self.cgst = cgst
			self.sgst = sgst
			self.save()

	def get_absolute_edit_url(self):
		return reverse("item:edit", kwargs={"pk" : self.pk})

	def get_absolute_url(self):
		return reverse("item:detail", kwargs={"pk" : self.pk})
	# method for updating

def postUpdateItem(sender, instance, **kwargs):
	post_save.disconnect(postUpdateItem, sender=sender)
	try:
		instance.use_date = timezone.now()
		instance.use_time = timezone.now()

		chain_id_name = instance.group_id.name
		company = Company.objects.get(name = chain_id_name)
		instance.company_id = company
		if not instance.item_code:
			instance.item_code = create_item_code()
		conv = int(instance.unit_id.number)
		if instance.nos_stock >= conv:
			instance.strip_stock += int((instance.nos_stock)//conv)
			instance.nos_stock    = int((instance.nos_stock)%conv)

		instance.save()
	except:
		pass
		
	post_save.connect(postUpdateItem, sender=sender)

post_save.connect(postUpdateItem, sender = Item)



class Batch(models.Model):
	item_id = 		models.ForeignKey(Item, null=True, blank=True, db_index=True)
	batch_no = 		models.CharField(max_length = 15, db_index = True)
	strip = 		models.IntegerField(null = True, blank = True, default = 0)
	nos = 			models.IntegerField(null = True, blank = True, default = 0)
	expiry = 		models.DateField()
	strip_pur = 	models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)
	strip_sale = 	models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)
	mrp = 			models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)
	sale_rt = 		models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)
	inst_rt = 		models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)
	trade_rt = 		models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)

	std_rt = 		models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)
	pur_rt = 		models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0.00)

	tot_rec_qty =	models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0) #No use
	tot_iss_qty =	models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, default = 0)	#No use

	conv =			models.IntegerField(null = True, blank = True)
	td = 			models.IntegerField(null = True, blank = True, default = 1)

	class Meta:
		unique_together = ['item_id', 'batch_no']
		verbose_name = 'Batch'
		verbose_name_plural = 'Batches'
		unique_together = ("batch_no", "item_id")

	def __str__(self):
		return self.batch_no

	def handle_BatchQty_Stock_OnAdd(self, strip, nos, *args, **kwargs):

		total_qty_old = (self.strip)*(self.conv) + self.nos
		total_qty_new = total_qty_old + strip*(self.conv) + nos
		if total_qty_new > 0:
			self.strip = (total_qty_new)//(self.conv)
			self.nos = (total_qty_new)%(self.conv)
		else:
			total_qty_new = abs(total_qty_new)
			self.strip = (-1)*((total_qty_new)//(self.conv))
			self.nos = (-1)*((total_qty_new)%(self.conv))

		self.save()

	def handle_BatchQty_Stock_OnSub(self, strip, nos, *args, **kwargs):
		total_qty_old = (self.strip)*(self.conv) + self.nos
		total_qty_new = total_qty_old - strip*(self.conv) - nos

		if total_qty_new > 0:
			self.strip = (total_qty_new)//(self.conv)
			self.nos = (total_qty_new)%(self.conv)
		else:
			total_qty_new = abs(total_qty_new)
			self.strip = (-1)*((total_qty_new)//(self.conv))
			self.nos = (-1)*((total_qty_new)%(self.conv))

		self.save()


def post_update_batch(sender, instance, **kwargs):
	post_save.disconnect(post_update_batch, sender=sender)
	try:
		if not instance.conv or instance.conv != instance.item_id.unit_id.number:	#save conv
			instance.conv = instance.item_id.unit_id.number
		if instance.nos >= instance.conv:
			instance.strip += (instance.nos)//(instance.conv)
			instance.nos = (instance.nos)%(instance.conv)

		instance.save()
	except:
		pass

	post_save.connect(post_update_batch, sender = Batch)

post_save.connect(post_update_batch, sender = Batch)
