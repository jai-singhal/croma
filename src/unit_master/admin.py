from django.contrib import admin
from .models import Unit

class UnitModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name",  "number"]
    list_display_links = ["name"]
    search_fields  = ["name"]
    search_fields = ["id", "name", "number"]


admin.site.register(Unit, UnitModelAdmin)