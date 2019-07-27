from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.
class Salt(models.Model):
	name = 		models.CharField(max_length = 250, unique = True, db_index = True)
	use_date = 	models.DateField(null = True, blank = True)
	user_id = 	models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_time = 	models.TimeField(null = True, blank = True)
	class Meta:
	    verbose_name = 'Salt'
	    verbose_name_plural = 'Salts'
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Salt, self).save(*args, **kwargs)	