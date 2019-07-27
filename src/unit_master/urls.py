from django.conf.urls import url, include
from .views import UnitCreate


urlpatterns = [
	url(r'^api/', include("unit_master.api.urls"), name = 'unit-api'),
	url(r'^create$', UnitCreate, name = "create"),

]