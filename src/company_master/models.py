from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from godown_master.models import Godown
from django.shortcuts import get_object_or_404
from accounts.models import Accounts, Head

class Supplier(models.Model):
	name =			models.CharField(max_length = 150, unique = True, db_index = True)
	person =		models.CharField(max_length = 150, null = True, blank = True)
	add1 = 			models.CharField(max_length = 150, null = True, blank = True)
	add2 = 			models.CharField(max_length = 150, null = True, blank = True)
	add3 = 			models.CharField(max_length = 150, null = True, blank = True)
	city = 			models.CharField(max_length = 60, null = True, blank = True)
	phone1 = 		models.CharField(max_length = 12, null = True, blank = True)
	phone2 = 		models.CharField(max_length = 12, null = True, blank = True)

	lst_num = 		models.CharField(max_length = 12, null = True, blank = True)
	cst_num = 		models.CharField(max_length = 12, null = True, blank = True)

	drug_license1 = models.CharField(max_length = 40, null = True, blank = True)
	drug_license2 = models.CharField(max_length = 40, null = True, blank = True)
	tin_no = 		models.CharField(max_length = 40, null = True, blank = True)
	pin_no =	 	models.CharField(max_length = 40, null = True, blank = True)

	gst_no = 		models.CharField(max_length = 15, null = True, blank = True)

	c_days = 		models.IntegerField(default = 0, null = True, blank = True) #CREDIT DAY
	c_limit = 		models.DecimalField(max_digits=10, decimal_places=2, default = 0, null = True, blank = True) #Credit Amount

	user_id =  		models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date = 		models.DateField(null = True, blank = True)
	account_id = 	models.ForeignKey(Accounts, default = 1)
	head_id =		models.ForeignKey(Head, default = 22)
	less_by = 		models.IntegerField(default = 0, null = True, blank = True)
	use_time = 		models.TimeField(null = True, blank = True)
	identity = 		models.CharField(max_length = 30, null = True, blank = True) #NULL FIELD

	class Meta:
	    verbose_name = 'Supplier'
	    verbose_name_plural = 'Suppliers'

	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Supplier, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Chain(models.Model):
	name = 		models.CharField(max_length = 150, unique = True, db_index = True)
	master = 	models.IntegerField(default = 0, blank = True, null = True)
	group = 	models.IntegerField(default = 0, blank = True, null = True)
	full_path = models.CharField(max_length = 200, default = 'TOP')
	nodes = 	models.IntegerField(default = 0, blank = True, null = True)
	category = 	models.CharField(max_length = 50, default = 'COMPANY', blank = True, null = True)
	total = 	models.IntegerField(default = 0, blank = True, null = True)
	user_id = 	models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date = 	models.DateField(null = True, blank = True)
	use_time = 	models.TimeField(null = True, blank = True)

	class Meta:
	    verbose_name = 'Chain'
	    verbose_name_plural = 'Chains'

	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Chain, self).save(*args, **kwargs)

	def increase_total(self, *args, **kwargs):
		self.total += 1
		self.save()

	def __str__(self):
		return self.name


class Company(models.Model):
	name = 			models.CharField(max_length = 150, unique = True, db_index = True)
	short_name = 	models.CharField(max_length = 80, null = True, blank = True)
	add1 = 			models.CharField(max_length = 150, null = True, blank = True)
	add2 = 			models.CharField(max_length = 150, null = True, blank = True)
	add3 = 			models.CharField(max_length = 150, null = True, blank = True)

	city = 			models.CharField(max_length = 60, null = True, blank = True)
	phone1 = 		models.CharField(max_length = 12, null = True, blank = True)
	phone2 = 		models.CharField(max_length = 12, null = True, blank = True)
	chain_id = 		models.ForeignKey(Chain, default=1)
	godown_id = 	models.ForeignKey(Godown, default = 1)
	ptax = 			models.IntegerField(default = 5, null = True, blank = True)    #XXXX Why 5?

	user_id = 		models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null = True, blank = True)
	use_date =		models.DateField(null = True, blank = True)

	use_time = 		models.TimeField(null = True, blank = True)
	supp_id = 		models.ForeignKey(Supplier, default = 1, on_delete = models.SET_DEFAULT)
	stax = 			models.IntegerField(default = 3, null = True, blank = True)


	class Meta:
	    verbose_name = 'Company'
	    verbose_name_plural = 'Companies'
	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()

		if self.pk is not None: #That is, Update query
			orig = Company.objects.get(pk=self.pk)
			if orig.name != self.name:
				old_chain = Chain.objects.get(name = str(orig.name))
				old_chain.name = str(self.name) #Changing the name of chain
				old_chain.save()

		else:		#Creating a new company
			obj = Chain.objects.create(name = self.name)

		return super(Company, self).save(*args, **kwargs)
	def __str__(self):
		return self.name

def post_save_company(sender, instance, **kwargs):
	post_save.disconnect(post_save_company, sender=sender)
	instance.chain_id = Chain.objects.get(name = instance.name)
	instance.save()
	post_save.connect(post_save_company, sender=sender)

post_save.connect(post_save_company, sender = Company)
