from django.contrib import admin
from .models import *


class SaleInvHrdModelAdmin(admin.ModelAdmin):

    list_display = ["id", "doc_no", "doc_dt",  "party_id_name", 
    				"doctor_id_name", "mode", "net_amount", "session_id"]
    list_display_links = ["doc_no"]

    list_filter = ["doc_dt",]
    search_fields = ["doc_no", "id", "party_id__name", "doctor_id__name"]

    def party_id_name(self, obj):
        return obj.party_id.name
    def doctor_id_name(self, obj):
        return obj.doctor_id.name

    class Meta:
        model = SalesInvHrd


class SaleInvDtlModelAdmin(admin.ModelAdmin):
	
    list_display = ["sequence", "hrd_id",  "item_name", 
    				"batch_no", "strip_qty", "nos_qty", "strip_free", "nos_free", "amount"]
    # list_display_links = ["doc_no"]

    search_fields = ["sequence", "hrd_id__id", "item_id__name"]

    def item_name(self, obj):
        return obj.item_id.name

    class Meta:
        model = SalesInvDtl


admin.site.register(Doctor)
admin.site.register(Party)
admin.site.register(SalesInvHrd, SaleInvHrdModelAdmin)
admin.site.register(SalesInvDtl, SaleInvDtlModelAdmin)
