from django.contrib import admin
from .models import *


class YearEndingdModelAdmin(admin.ModelAdmin):

	list_display = ["id", "code", "year_pur_id", "year_sale_id",  "from_dt", 
					"to_dt", "registration_id_" ]
	list_display_links = ["code"]

	list_filter = ["code"]
	search_fields = ["code", "id"]

	def registration_id_(self, obj):
	    return str(obj.registration_id.id)

	class Meta:
	    model = YearEnding



admin.site.register(Registration)
admin.site.register(Accounts)
admin.site.register(Head)
#admin.site.register(UserProfile)
admin.site.register(YearEnding, YearEndingdModelAdmin)