from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^register', register_view, name = "register_view"),
    url(r'^login', loginView.as_view(), name = "login"),
    url(r'^logout', logout_view, name = "logout"),
    url(r'^company/register', companyRegistrationView, name="company-register"),
    url(r'^session/expire', sessionExpireView.as_view(), name="sessionExpireView"),
]
