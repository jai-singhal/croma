from django.conf.urls import url, include
from .views import *

urlpatterns = [
	url(r'^create/$', CreatePurchase.as_view(), name = "create"),
	url(r'^(?P<pk>\d+)$', RetrievePurchase, name = "detail"),
	url(r'^(?P<pk>\d+)/edit$', UpdatePurchase.as_view(), name = "edit"),
	#url(r'^(?P<pk>\d+)/delete$', DeleteSale, name = "delete"),
	url(r'^ajax/search_inv$', SearchInv, name = "SearchInv"),

	url(r'^ajax/delete_inv$', DeletePurchase, name = "DeletePurInv"),
	url(r'^ajax/checkSupplieNameInv$', checkSupplierNameInv, name="checkSupplierNameInv"),

]
