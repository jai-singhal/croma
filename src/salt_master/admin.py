from django.contrib import admin
from .models import Salt

class SaltModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    list_display_links = ["name"]

    search_fields  = ["id", "name"]


    class Meta:
        model = Salt
        ordering = ['-id',]

admin.site.register(Salt, SaltModelAdmin)