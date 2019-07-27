from django.contrib import admin
from .models import Item, Batch, TaxType


class ItemModelAdmin(admin.ModelAdmin):

    list_display = ["id", "item_code",  "name",
                    "unit", "company", "salt", "strip_stock", "nos_stock"]
    list_display_links = ["name"]

    search_fields = ["name", "id"]

    def unit(self, obj):
        return obj.unit_id.name

    def company(self, obj):
        return obj.company_id.name

    def salt(self, obj):
        return obj.salt_id.name

    class Meta:
        model = Item
        ordering = ['-id', 'name', 'use_date']
        readonly_fields = ('item_code')


class BatchModelAdmin(admin.ModelAdmin):

    list_display = ["id", "item_name", "batch_no",  "expiry",
                    "strip", "nos", "mrp"]
    list_display_links = ["batch_no"]

    search_fields = ["batch_no", "id", "item_id__name"]

    def item_name(self, obj):
        return obj.item_id.name

    class Meta:
        model = Batch


admin.site.register(TaxType)
admin.site.register(Item, ItemModelAdmin)
admin.site.register(Batch, BatchModelAdmin)
