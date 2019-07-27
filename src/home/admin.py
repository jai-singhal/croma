from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from accounts.forms import UserLoginForm
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Register your models here.
AdminSite.site_header = "Croma"
AdminSite.site_title = "Croma"
# AdminSite.login_form = UserLoginForm
# AdminSite.login_template = os.path.join(BASE_DIR, 'templates/accounts/account_form.html')



