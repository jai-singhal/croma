from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.
class Unit(models.Model):
	name = 		models.CharField(max_length = 30, unique = True, db_index = True)
	number = 	models.IntegerField()
	shrt_unit = models.CharField(max_length = 30, null = True, blank = True)
	detail = 	models.CharField(max_length = 100, null = True, blank = True)
	user_id = 	models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_date = 	models.DateField(null = True, blank = True)
	use_time = 	models.TimeField(null = True, blank = True)
	class Meta:
	    verbose_name = 'Unit'
	    verbose_name_plural = 'Units'

	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Unit, self).save(*args, **kwargs)
	def __str__(self):
		return self.name