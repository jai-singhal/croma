from django.conf.urls import url
from .views import GodownCreate

urlpatterns = [
	url(r'^create/$', GodownCreate, name = "create"),

]
