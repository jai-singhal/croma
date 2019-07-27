from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'^api/', include("company_master.api.urls"), name = "company-api"),
	url(r'^create$', CompanyCreate, name = "create"),
	url(r'^(?P<pk>\d+)/edit', CompanyEdit, name = "edit"),

	url(r'^supplier/create$', SupplierCreate, name = "create"),
	url(r'^supplier/(?P<pk>\d+)/edit', SupplierEdit, name = "edit"),

	#AJAX
	url(r'^ajax/get_company_id$', get_company_id, name = "get_company_id"),
	url(r'^ajax/get_supplier_id$', get_supplier_id, name = "get_supplier_id"),
	url(r'^ajax/get_company_info$', get_company_info, name = "get_company_info"),

]