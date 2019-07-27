from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'^list/$',	UnitListApiView.as_view(), name = "list"),
]
