from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^account/', include("accounts.urls", namespace = 'account')),
    url(r'^reports/', include("reports.urls", namespace = 'reports')),
	url(r'^sales/', include("sales.urls", namespace = 'sales')),
	url(r'^purchase/', include("purchase.urls", namespace = 'purchase')),
	url(r'^item/', include("item_master.urls", namespace = 'item')),
	url(r'^company/', include("company_master.urls", namespace = 'company')),
	url(r'^salt/', include("salt_master.urls", namespace = 'salt')),
	url(r'^godown/', include("godown_master.urls", namespace = 'godown')),
	url(r'^unit/', include("unit_master.urls", namespace = 'unit')),

	url(r'^', include("home.urls", namespace = 'home')),

]


