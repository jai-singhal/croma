from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'^list/$', SaltListApiView.as_view(), name = "list"),
]
