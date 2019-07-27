from django.conf.urls import url  
from .views import HomePage, takeBackup


urlpatterns = [
    url(r'^$', HomePage, name = "home"),
    url(r'ajax/backup', takeBackup, name = "takeBackup"),
    
]