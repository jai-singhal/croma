try:
	import urllib.parse
except:
	from urlparse import urlparse
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Company, Chain, Supplier
from .forms import CompanyForm, SupplierForm
from django.views import View
import json

def CompanyCreate(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	form = CompanyForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_group_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
		"title": "Company Form"
	}
	return render(request, "company_master/create.html", context)

def CompanyEdit(request, pk = None):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Company, pk = pk)
	form = CompanyForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_group_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
		"title": "Company Form"
	}
	return render(request, "company_master/create.html", context)

def get_company_id(request):
	if request.is_ajax():
		company_name = request.GET['company_name']
		chain_id = Company.objects.get(name = company_name).id
		data = {
			'chain_id':str(chain_id),
		}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

def SupplierCreate(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	form = SupplierForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_supplier_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
		"title": "Supplier Form"
	}
	return render(request, "company_master/create.html", context)

def SupplierEdit(request, pk = None):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Supplier, pk = pk)
	form = SupplierForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_supplier_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
		"title": "Supplier Form"
	}
	return render(request, "company_master/create.html", context)

def get_supplier_id(request):
	if request.is_ajax():
		supplier_name = request.GET['supplier_name']
		supplier_id = Supplier.objects.get(name = supplier_name).id
		data = {
			'supplier_id':str(supplier_id),
		}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")


def get_company_info(request):
	if request.method == "GET" and request.is_ajax():
		company = request.GET.get("company_name")
		instance = Company.objects.get(name = company)
		context = {
			"name": company,
			"add1": instance.add1,
			"add2": instance.add2,
			"city": instance.city,
			"supplier": {
				"name": instance.supp_id.name,
				"add1": instance.supp_id.add1,
				"add2": instance.supp_id.add2,
				"city": instance.supp_id.city,
				"drug_license1": instance.supp_id.drug_license1,
				"drug_license2": instance.supp_id.drug_license2,
				"tin_no": instance.supp_id.tin_no,
				"gst_no": instance.supp_id.gst_no,
				"pin_no": instance.supp_id.pin_no,
				"lst_num": instance.supp_id.lst_num,
				"cst_num": instance.supp_id.cst_num,
			}
		}
		return JsonResponse(context, status = 200)
	return JsonResponse({}, status = 400)