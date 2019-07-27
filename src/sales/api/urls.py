from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'^party-list/$',	PartyListApiView.as_view(), name = "party-list"),
	url(r'^doctor-list/$',	DoctorListApiView.as_view(), name = "doctor-list"),
]
