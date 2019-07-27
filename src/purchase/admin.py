from django.contrib import admin
from .models import *

class PurchaseInvHrdModelAdmin(admin.ModelAdmin):

    list_display = ["id", "doc_no", "doc_dt",  "supplier_id_name", 
    				"supp_chal_no","net_amount", "paid_amount", "session_id"]
    list_display_links = ["doc_no"]

    search_fields = ["doc_no", "id"]

    def supplier_id_name(self, obj):
        return obj.supplier_id.name

    class Meta:
        model = PurchaseInvHrd


class PurInvDtlModelAdmin(admin.ModelAdmin):
	
    list_display = ["id", "hrd_id",  "item_name", 
    				"batch_no", "strip_qty", "nos_qty", "strip_free", "nos_free", "discount", "amount"]
    list_display_links = ["hrd_id"]

    search_fields = ["id", "hrd_id__id"]

    def item_name(self, obj):
        return obj.item_id.name

    class Meta:
        model = PurchaseInvDtl


admin.site.register(PurchaseInvHrd, PurchaseInvHrdModelAdmin)
admin.site.register(PurchaseInvDtl, PurInvDtlModelAdmin)

