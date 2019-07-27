from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Salt
from .forms import SaltForm
from django.views import View
import json

# Create your views here.
def SaltCreate(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	form = SaltForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_salt_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
	}
	return render(request, "salt_master/create.html", context)

def SaltEdit(request, pk = None):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Salt, pk = pk)
	form = SaltForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_salt_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
	}
	return render(request, "salt_master/create.html", context)

def get_salt_id(request):
	if request.is_ajax():
		salt_name = request.GET['salt_name']
		salt_id = Salt.objects.get(name = salt_name).id
		data = {
			'salt_id':str(salt_id),
		}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")
