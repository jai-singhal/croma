from django.conf.urls import url, include
from .views import *

urlpatterns = [
	url(r'^api/', include("item_master.api.urls"), name = "item-api"),
	url(r'^create/$', CreateItem.as_view(), name = "create"),
	url(r'^(?P<pk>\d+)$', RetrieveItem, name = "detail"),
	url(r'^(?P<pk>\d+)/edit$', UpdateItem.as_view(), name = "edit"),
	url(r'^ajax/search_item$', search_item, name = "search_item"),
	url(r'^ajax/get/item_batches$', get_item_batches, name = "get_item_batches"),
	url(r'^ajax/delete_item$', DeleteItem, name = "delete_item"),
	url(r'^ajax/search/item_info$', search_item_info, name = "search_item_info"),
]
