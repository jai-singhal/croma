try:
	import urllib.parse
except:
	from urlparse import urlparse
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Godown
from .forms import GodownForm
from django.views import View
import json

# Create your views here.
def GodownCreate(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	form = GodownForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_godown_id");</script>' % (pk_value, instance))
	context = {
		"form" : form,
	}
	return render(request, "godown_master/create.html", context)