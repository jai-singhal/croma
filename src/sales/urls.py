from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'^api/', include("sales.api.urls"), name = "sales-api"),
	url(r'^create/$', CreateSale.as_view(), name = "create"),
	url(r'^(?P<pk>\d+)$', RetrieveSale, name = "detail"),
	url(r'^(?P<pk>\d+)/edit$', UpdateSale.as_view(), name = "edit"),

	#ajax
	url(r'^view_invoice$', ViewInvoice, name = "ViewInvoice"),
	url(r'^print_invoice$', PrintInvoice, name = "PrintInvoice"),
	url(r'^ajax/search_inv$', SearchInv, name = "SearchInv"),

	url(r'^ajax/delete_inv$', DeleteSale, name = "DeleteSaleInv"),

#Doctor Crud System Urls
	url(r'^doctor/create$', DoctorCreate, name = "doctor_create"),
	url(r'^doctor/(?P<pk>\d+)/edit', DoctorEdit, name = "doctor_edit"),
	#AJAX
	url(r'^doctor/ajax/get_doctor_id$', get_doctor_id, name = "get_doctor_id"),
]
