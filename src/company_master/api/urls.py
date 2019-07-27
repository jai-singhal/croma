from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'^chain-list/$', ChainListApiView.as_view(), name = "chain-list"),
	url(r'^company-list/$',	CompanyListApiView.as_view(), name = "company-list"),
	url(r'^supplier-list/$', SupplierListApiView.as_view(), name = "supplier-list"),
]
