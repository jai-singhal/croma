from django.db import models
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Head(models.Model):
	headname =		models.CharField(max_length = 150, unique = True)
	parent_id = 	models.IntegerField(null = True, blank = True)
	show =			models.CharField(max_length = 5, null = True, blank = True)
	alias =			models.CharField(max_length = 50, null = True, blank = True)
	use_date = 		models.DateField(null = True, blank = True)
	use_time = 		models.TimeField(null = True, blank = True)
	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Head, self).save(*args, **kwargs)
	def __str__(self):
		return self.headname


class Accounts(models.Model):
	name =				models.CharField(max_length = 150, unique = True)
	alias_name =		models.CharField(max_length = 30, null = True, blank = True)
	head_id = 			models.ForeignKey(Head)
	OpeningBalance = 	models.DecimalField(max_digits=12, decimal_places=4, default = 0, null = True, blank = True)
	ItNo = 				models.CharField(max_length = 30, null = True, blank = True)
	StNo = 				models.CharField(max_length = 30, null = True, blank = True)
	Type = 				models.CharField(max_length = 5, null = True, blank = True)
	category =			models.CharField(max_length = 30, null = True, blank = True )
	Current_Balance = 	models.DecimalField(max_digits=12, decimal_places=4, default = 0, null = True, blank = True)
	user_id =  			models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date = 			models.DateField(null = True, blank = True)
	use_time = 			models.TimeField(null = True, blank = True)
	
	class Meta:
	    verbose_name = 'Account'
	    verbose_name_plural = 'Accounts'

	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Accounts, self).save(*args, **kwargs)
	def __str__(self):
		return self.name

class Registration(models.Model):
	company_name = 	models.CharField(max_length = 100)
	address1 =		models.CharField(max_length = 100, null = True, blank = True)
	address2 = 		models.CharField(max_length = 100, null = True, blank = True)
	address3 = 		models.CharField(max_length = 100, null = True, blank = True)
	city = 			models.CharField(max_length = 80, blank = True, null = True)
	state = 		models.CharField(max_length = 80, blank = True, null = True)
	country = 		models.CharField(max_length = 80, blank = True, null = True)
	pin = 			models.CharField(max_length = 10, blank = True, null = True)
	phone1 = 		models.CharField(max_length = 12, blank = True, null = True)
	phone2 = 		models.CharField(max_length = 12, blank = True, null = True)
	phone3 = 		models.CharField(max_length = 12, blank = True, null = True)
	website = 		models.CharField(max_length = 50, blank = True, null = True)
	dl_no1 = 		models.CharField(max_length = 30, blank = True, null = True)
	dl_no2 = 		models.CharField(max_length = 30, blank = True, null = True)
	email_id = 		models.EmailField(null = True, blank = True)
	lst = 			models.CharField(max_length = 50, blank = True, null = True)
	cst = 			models.CharField(max_length = 50, blank = True, null = True)
	gst_no =		models.CharField(max_length = 50, blank = True, null = True)
	tin_no = 		models.CharField(max_length = 50, blank = True, null = True)
	user_id =  		models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

	def __str__(self):
		return self.company_name


class YearEnding(models.Model):
	code = 			models.CharField(max_length = 15, unique = True)
	year_pur_id = 	models.IntegerField(blank = True, null = True)
	year_sale_id = 	models.IntegerField(blank = True, null = True)
	from_dt = 		models.DateField()
	to_dt = 		models.DateField()
	registration_id = models.ForeignKey(Registration, default = 1)
	
	def __str__(self):
		return self.code + ",   Year = [ " + str(self.from_dt.year) + " to " + str(self.to_dt.year) + " ]"

	def get_absolute_report1_url(self):
		return reverse("reports:report1_url", kwargs={"from_dt" : self.from_dt, "to_dt": self.to_dt})

