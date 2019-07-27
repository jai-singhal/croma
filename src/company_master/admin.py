from django.contrib import admin
from .models import Supplier, Company, Chain
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    list_display_links = ["name"]

    search_fields  = ["id", "name"]


    class Meta:
        model = Company
        ordering = ['-id',]

class ChainModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    list_display_links = ["name"]

    search_fields  = ["id", "name"]


    class Meta:
        model = Chain
        ordering = ['-id',]

class SupplierModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    list_display_links = ["name"]

    search_fields  = ["id", "name"]


    class Meta:
        model = Supplier
        ordering = ['-id',]

# Register your models here.
admin.site.register(Chain, ChainModelAdmin)
admin.site.register(Supplier, SupplierModelAdmin)
admin.site.register(Company, CompanyModelAdmin)