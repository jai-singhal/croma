from django.conf.urls import url, include
from .views import SaltCreate, SaltEdit, get_salt_id


urlpatterns = [
	url(r'^api/', include("salt_master.api.urls"), name = "salt-api"),
	url(r'^create$', SaltCreate, name = "create"),
	url(r'^(?P<pk>\d+)/edit', SaltEdit, name = "edit"),

	#AJAX
	url(r'^ajax/get_salt_id$', get_salt_id, name = "get_salt_id"),
]
