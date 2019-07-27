try:
	import urllib.parse
except:
	from urlparse import urlparse
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Unit
from .forms import UnitForm
from django.views import View
import json



def UnitCreate(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	form = UnitForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_unit_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
	}
	return render(request, "unit_master/create.html", context)