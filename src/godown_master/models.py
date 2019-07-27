from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils import timezone

class Godown(models.Model):
	name = 		models.CharField(max_length = 50, unique = True)
	use_date = 	models.DateField(null = True, blank = True)
	user_id = 	models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	use_time = 	models.TimeField(null = True, blank = True)
	class Meta:
	    verbose_name = 'Godown'
	    verbose_name_plural = 'Godowns'

	def save(self, *args, **kwargs):
		if not self.id:
			self.use_date = timezone.now()
			self.use_time = timezone.now()
		return super(Godown, self).save(*args, **kwargs)
	def __str__(self):
		return self.name
