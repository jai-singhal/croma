from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views import View
from django.core.serializers import serialize
from django.views.generic import UpdateView
from django.conf import settings
import json
import os
import logging
import subprocess as sp
import sys

from item_master.models import Item, Batch
from .models import *
from .forms import *
from .serializers import *
from .models import Party, Doctor
from .utils import create_SaleInvDtl_JSON_QuerySet
from .print_inv import MakeInvoice
from accounts.models import YearEnding

logger = logging.getLogger(__name__)

class CreateSale(View, LoginRequiredMixin):
	login_url = '/account/login/'
	template_name = 'sales/index.html'

	def get(self, request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(self.login_url)

		saleInvHrdForm = SalesInvHrdForm(request.POST or None)
		saleInvDtlForm = SalesInvDtlForm(request.POST or None)
		current_session = get_object_or_404(YearEnding, id=request.session['session'])
		try:
			prev_sale = SalesInvHrd.objects.filter(session_id=current_session).order_by('-id').first()
			doc_no = prev_sale.doc_no + 1
		except Exception as e:
			logger.error(e)
			prev_sale = None
			doc_no = 1
		context = {
			"form" : saleInvHrdForm,
			"item_form" : saleInvDtlForm,
			"prev" : prev_sale,
			"doc_no": doc_no,
			'is_create': True,
			"current_session":current_session
		}
		return render(self.request, self.template_name, context)

	# @transaction.atomic
	def post(self, request):
		if not request.user.is_authenticated():
			raise Http404
		# sid = transaction.savepoint()
		try:
			with transaction.atomic():
				session_id = request.session['session']
				if self.request.method == "POST" and self.request.is_ajax():
					json_dict = json.loads( request.body.decode('utf-8'))
					sale_info, sale_items = json_dict['sale_info'], json_dict['item_table']
					for i, item in enumerate(sale_items):
						if item['deleted'] == 1:
							del sale_items[i]

					errors = []
					try:
						next_doc_no = SalesInvHrd.objects.filter(session_id=session_id).order_by('-id').first().doc_no + 1
					except Exception as e:
						logger.error(str(e))
						next_doc_no = 1
					sale_info['session_id'], sale_info['doc_no'] = session_id, next_doc_no

					serializer_sale_hrd =  SalesInvHdrSerialzer(data=sale_info)

					if serializer_sale_hrd.is_valid():
						sale_hrd_obj = serializer_sale_hrd.save()
					else:
						# transaction.savepoint_rollback(sid)
						errors.append(serializer_sale_hrd.errors)
						response = {'status': 0, 'errors':errors}
						return JsonResponse(response, status=400)

					#Handling Item Table Populating Hrd Table
					for item in sale_items:
						item_id = item['item_id']
						if Item.objects.filter(id = item_id).exists():
							item_obj = Item.objects.get(id = item_id)
							total_strip, total_nos = int(item['strip_qty']) + int(item['strip_free']), int(item['nos_qty']) + int(item['nos_free'])
							#Subtract from strip and nos stock of Item Database
							item_obj.handle_ItemQty_Stock_OnSub(total_strip, total_nos)
							# Subtracting the qty [nos and strip] from batch Table
							if Batch.objects.filter(batch_no = item['batch_no'], item_id = item_obj).exists():
								item_batch = Batch.objects.get(batch_no = item['batch_no'], item_id = item_obj)
								item_batch.handle_BatchQty_Stock_OnSub(total_strip, total_nos)
							else:
								pur_rate, mrp = float(item['pur_rate']), float(item['mrp'])
								Batch.objects.create(item_id = item_obj,
																batch_no = item['batch_no'], expiry = item['expiry'],
																strip = 0, nos= 0,
																strip_pur = pur_rate, strip_sale = mrp,
																mrp = mrp, sale_rt = mrp*0.1, inst_rt = mrp,
																trade_rt = mrp, std_rt = mrp, pur_rt = pur_rate*0.1
																)
						else:
							response = {'errors':"Item name '{}' is required".format(item["item_name"])}
							return JsonResponse(response, status=400)

						item['hrd_id'] = sale_hrd_obj.id
						serializer_sale_dtl = SalesInvDtlSerialzer(data=item)
						if serializer_sale_dtl.is_valid():
							serializer_sale_dtl.save()
						else:
							errors.append(serializer_sale_dtl.errors)
							response = {'status': 0, 'errors':errors}
							return JsonResponse(response, status=400)

					response = {
						'status': 1,
						'message': "Successfully Saved",
						'url' : sale_hrd_obj.get_absolute_url(),
					}
					return JsonResponse(response, status=200)
		except Exception as e:
			logger.error("Error on line {} \nType: {} \nError:{}".format(sys.exc_info()[-1], type(e).__name__, str(e)))
			return JsonResponse({"errors": str(e)}, status=400)



@login_required(login_url='/account/login/')
def RetrieveSale(request, pk = None):
	if not request.user.is_authenticated():
		raise Http404

	current_session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id = current_session_id)

	saleInvDtlForm = SalesInvDtlForm(request.POST or None)
	#Get the sale inv Query
	instance = get_object_or_404(SalesInvHrd, id = pk, session_id = current_session)
	doc_no = instance.doc_no
	saleInvhrd_form = SalesInvHrdForm(request.POST or None, instance = instance)
	#Get the respective Items Query
	saleInvDtl_queryset = SalesInvDtl.objects.filter(hrd_id = pk)	#Queryset of all items assocuadted with hrd_id = pk
	sale_dtl_item_arr = create_SaleInvDtl_JSON_QuerySet(saleInvDtl_queryset)	#create a dict of all sale item for respective invoice
	saleDtl_item_set_json = json.dumps(sale_dtl_item_arr)	#get the json data for all items

	saleInvhrd_form.initial["doctor_id"] = instance.doctor_id.name
	saleInvhrd_form.initial["party_id"] = instance.party_id.name

	try:
		next_sale_inv = SalesInvHrd.objects.filter(id__gt = pk,session_id = current_session).order_by("pk").first()
	except:		next_sale_inv = None
	try:
		prev_sale_inv = SalesInvHrd.objects.filter(id__lt = pk, session_id = current_session).order_by("-pk").first()
	except:		prev_sale_inv = None

	context = {
			"is_retrieve":True,
			"saleDtl_item_set_json": saleDtl_item_set_json,
			"doc_no": doc_no,
			"instance": instance,
			"form" : saleInvhrd_form,
			"item_form" : saleInvDtlForm,
			"prev": prev_sale_inv,
			"next":next_sale_inv,
			"current_session":current_session
	}

	return render(request, "sales/index.html", context)


class UpdateSale(UpdateView, LoginRequiredMixin):
	template_name = 'sales/index.html'
	login_url = '/account/login/'

	def get(self, request, pk = None):
		if not request.user.is_authenticated():
			raise Http404
		current_session_id = request.session['session']
		current_session = get_object_or_404(YearEnding, id = current_session_id)

		saleInvDtlForm = SalesInvDtlForm(request.POST or None)
		#Get the sale inv Query
		instance = get_object_or_404(SalesInvHrd, id = pk)
		doc_no = instance.doc_no

		saleInvhrd_form = SalesInvHrdForm(request.POST or None, instance = instance)

		#Get the respective Items Query
		saleInvDtl_queryset = SalesInvDtl.objects.filter(hrd_id = pk)	#Queryset of all items assocuadted with hrd_id = pk
		sale_dtl_item_arr = create_SaleInvDtl_JSON_QuerySet(saleInvDtl_queryset)	#create a dict of all sale item for respective invoice
		saleDtl_item_set_json = json.dumps(sale_dtl_item_arr)	#get the json data for all items
		
		saleInvhrd_form.initial["doctor_id"] = instance.doctor_id.name
		saleInvhrd_form.initial["party_id"] = instance.party_id.name

		context = {
				"is_update":True,
				"saleDtl_item_set_json": saleDtl_item_set_json,
				"doc_no": doc_no,
				"instance": instance,
				"form" : saleInvhrd_form,
				"item_form" : saleInvDtlForm,
				"current_session":current_session
		}
		return render(request, "sales/index.html", context)

	# @transaction.atomic
	def post(self, request, pk = None):
		if not request.user.is_authenticated():
			raise Http404

		# sid = transaction.savepoint()
		try:
			with transaction.atomic():
				if self.request.method == "POST" and self.request.is_ajax():
					#getting the jon array of saleinfo and sale_item_table_data
					json_dict = json.loads( request.body.decode('utf-8'))
					#taking off both form data
					current_session_id = request.session['session']
					sale_info, sale_items = json_dict['sale_info'], json_dict['item_table']
					sale_info['session_id'] = current_session_id
					errors = []
					try:
						sale_info_obj = SalesInvHrd.objects.get(id = pk)	#Getting the object of sale info from Db
					except Exception as e:
						logger.error(str(e))
						errors.append("No Sales Invoice Object Found in Database")
						response = {'status': 0, "errors": errors}
						return JsonResponse(response, status = 400)

					serializer_SaleInvHrd = SalesInvHdrSerialzer(sale_info_obj, data=sale_info)
					hrd_save_status = False
					if serializer_SaleInvHrd.is_valid():
						hrd_save_status = True
					else:
						# transaction.savepoint_rollback(sid)
						errors.append(serializer_SaleInvHrd.errors)
						response = {'status': 0, "errors": errors}
						return JsonResponse(response, status = 400)

					# Saving new item or update existing item
					# Handling Item Table. Changing The database according to new update: Create it or update it or delete it
					
					for item in sale_items:
						item_id = item['item_id']
						item['hrd_id'] = sale_info_obj.id
						if Item.objects.filter(id = item_id).exists():
							item_obj = Item.objects.get(id = item_id)
						else:
							# transaction.savepoint_rollback(sid)
							errors.append("Cannot able to find Item:"  + str(item['item_name']))
							return JsonResponse({"errors": errors}, status = 400)

						#Delete the Item if not present or status of deleted is True
						if item['deleted'] == 1:	#If Item is not present in ## Delete the Item
							if SalesInvDtl.objects.filter(hrd_id = pk, item_id = item_obj, batch_no = item['batch_no']).exists():
								SaleInvItem_instance = SalesInvDtl.objects.get(hrd_id = pk, item_id = item_obj, batch_no = item['batch_no'])
								strip, nos = SaleInvItem_instance.strip_qty + SaleInvItem_instance.strip_free, SaleInvItem_instance.nos_qty + SaleInvItem_instance.nos_free

								SaleInvItem_instance.delete()
								item_obj.handle_ItemQty_Stock_OnAdd(strip,nos)
								try:
									batch_instance = Batch.objects.get(item_id = item_obj, batch_no = item['batch_no'])
									batch_instance.handle_BatchQty_Stock_OnAdd(strip,nos)
								except Exception as e:
									logger.error(str(e))
									# transaction.savepoint_rollback(sid)
									errors.append("Smething went wrong"  + str(item['item_name']))
									response = {'status': 0, "errors": errors}
									return JsonResponse(response, status = 400)
							else:
								# transaction.savepoint_rollback(sid)
								errors.append("Cannot able to find Item Object"  + str(item['item_name']))
								response = {'status': 0, "errors": errors}
								return JsonResponse(response, status = 400)

						elif item['deleted'] == 0:
							#Create or Update the Item
							if Batch.objects.filter(item_id = item_obj, batch_no = item['batch_no']).exists():
								batch_obj = Batch.objects.get(item_id = item_obj, batch_no = item['batch_no'])
							else:
								pur_rate, mrp = float(item['pur_rate']), float(item['mrp'])
								try:
									batch_obj = Batch.objects.create(item_id = item_obj,
																batch_no = item['batch_no'], expiry = item['expiry'],
																strip = 0, nos= 0,
																strip_pur = pur_rate, strip_sale = mrp,
																mrp = mrp, sale_rt = mrp*0.1, inst_rt = mrp,
																trade_rt = mrp, std_rt = mrp, pur_rt = pur_rate*0.1
																)
								except Exception as e:
									logger.error(str(e))
									# transaction.savepoint_rollback(sid)
									errors.append("Error occured during creating a new Batch"  + str(item['item_name']))
									response = {'status': 0, "errors": errors}
									return JsonResponse(response, status = 400)

							total_strip_new, total_nos_new = int(item['strip_qty']) + int(item['strip_free']), int(item['nos_qty']) + int(item['nos_free'])

							# UPDATE THE Existing BATCH
							if SalesInvDtl.objects.filter(hrd_id = pk, batch_no = item['batch_no'], item_id = item['item_id']).exists():
								#getting the entery from DB  of hrd_id= pk, batch_no = item's batch_no and item_id = item_obj
								item_qs = SalesInvDtl.objects.get(hrd_id = pk, batch_no = item['batch_no'], item_id = item['item_id'])

								total_strip_old = item_qs.strip_qty + item_qs.strip_free
								total_nos_old = item_qs.nos_qty + item_qs.nos_free

								#Decrement the Stock Strip and Nos (New-old)
								item_obj.handle_ItemQty_Stock_OnSub(total_strip_new-total_strip_old, total_nos_new-total_nos_old)
								batch_obj.handle_BatchQty_Stock_OnSub(total_strip_new-total_strip_old, total_nos_new-total_nos_old)

								#serialize the item or update the item
								serializer_item = SalesInvDtlSerialzer(item_qs, data=item)

							else:	# CREATE THE NEW BATCH
								serializer_item = SalesInvDtlSerialzer(data = item)
								#Subtract from strip and nos stock of Item Database
								item_obj.handle_ItemQty_Stock_OnSub(total_strip_new, total_nos_new)
								# Subtracting the qty [nos and strip] from batch Table
								batch_obj.handle_BatchQty_Stock_OnSub(total_strip_new, total_nos_new)

							if serializer_item.is_valid(): #SAVE THE NEW OR UPDATE ITEM
								serializer_item.save()
							else:
								errors.append(serializer_item.errors)
								# transaction.savepoint_rollback(sid)
								response = {'status': 0,
											"errors": errors,
											"item":  str(item['item_name'])
											}
								return JsonResponse(response, status = 400)

					if hrd_save_status:
						SaleInvHrd_instance = serializer_SaleInvHrd.save()

					# transaction.savepoint_commit(sid)
					response = {
								'status': 1,
								'message': "Successfully Saved",
								'url' : SaleInvHrd_instance.get_absolute_url(),
							}
					return JsonResponse(response, status = 200)

				
				response = {'status': 0, "errors": ["Something went wrong",]}
				# transaction.savepoint_rollback(sid)
				return JsonResponse(response, status = 400)
		
		except Exception as e:
			# transaction.savepoint_rollback(sid)
			logger.error("Error on line {} \nType: {} \nError:{}".format(sys.exc_info()[-1], type(e).__name__, str(e)))
			return JsonResponse({"errors": str(e)}, status = 400)


def DeleteSale(request):
	if not request.user.is_authenticated():
		raise Http404
	current_session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id = current_session_id)

	if request.method == "POST" and request.is_ajax():

		json_dict = json.loads( request.body.decode('utf-8'))
		doc_no = json_dict['doc_no']
		errors = {}

		try:
			sale_inv_obj = SalesInvHrd.objects.get( session_id = current_session, doc_no = int(doc_no))
		except:
			errors['no_object'] = "Error: No Sale Invoice Object Found in Database"
			response = {'status': 0, "errors": errors}
			return JsonResponse(response, status = 400)

		last_obj = SalesInvHrd.objects.last()
		if last_obj != sale_inv_obj:
			errors['no_object'] = "Error: You cannot delete this Invoice"
			response = {'status': 0, "errors": errors}
			return JsonResponse(response, status = 400)			

		sale_dtl_qs = SalesInvDtl.objects.filter(hrd_id = sale_inv_obj)
		for obj in sale_dtl_qs:
			try:
				item_obj = Item.objects.get(id = obj.item_id.id)
				batch_obj = Batch.objects.get(item_id = item_obj, batch_no = obj.batch_no)
				batch_obj.handle_BatchQty_Stock_OnAdd(obj.strip_qty + obj.strip_free, obj.nos_qty + obj.nos_free)
				item_obj.handle_ItemQty_Stock_OnAdd(obj.strip_qty + obj.strip_free, obj.nos_qty + obj.nos_free)
			except:
				continue
			obj.delete()
		try:
			next_sale_inv = SalesInvHrd.objects.filter(id__gt = sale_inv_obj.id, session_id = current_session).order_by("pk").first()
			url = next_sale_inv.get_absolute_url()
		except:
			next_sale_inv = None
			url = "/sales/create"

		sale_inv_obj.delete()
		return JsonResponse({"status": 1, "url": url}, status = 200)

	return JsonResponse({"status": 0}, status = 400)



def ViewInvoice(request):
	if not request.user.is_authenticated():
		raise Http404
	if request.method == "POST" and request.is_ajax():
		json_dict = json.loads( request.body.decode('utf-8'))
		try:
			MakeInvoice(json_dict)
			file_path = getattr(settings, "PRINTINV_FILEPATH", None)
			osCommandString = f"notepad.exe {file_path}"
			os.system(osCommandString)
			response = {'status': 1,}
		except:
			response = {'status': 0,}
	else:
		response = {'status': 0,}
	if response['status']:
		return JsonResponse(response, status = 200)
	else:
		return JsonResponse(response, status = 400)



def PrintInvoice(request):
	if not request.user.is_authenticated():
		raise Http404
	
	file_path = getattr(settings, "PRINTINV_FILEPATH", None)
	if request.method == "POST" and request.is_ajax():
		json_dict = json.loads( request.body.decode('utf-8'))
		try:
			MakeInvoice(json_dict)
			os.startfile(file_path, "print")
			response = {'status': 1,}
		except:
			response = {'status': 0, "msg": "No Printer Connected to System"}
	else:
		response = {'status': 0,"msg":"Something went wrong"}

	if response['status']:
		return JsonResponse(response, status = 200)
	else:
		return JsonResponse(response, status = 400)



def SearchInv(request):
	if not request.user.is_authenticated():
		raise Http404
	current_session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id = current_session_id)

	if request.method == "GET" and request.is_ajax():
		inv_no = request.GET.get("sale_inv")
		if SalesInvHrd.objects.filter(session_id = current_session, doc_no = inv_no).exists():
			sale_inv_obj = SalesInvHrd.objects.get(session_id = current_session, doc_no = inv_no)
			response = {"status": 1, "msg" : sale_inv_obj.get_absolute_url()}
		else:
			response = {"status": 0, "msg": "No Invoice Found"}

	if response['status']:
		return JsonResponse(response, status = 200)
	else:
		return JsonResponse(response, status = 400)



def DoctorCreate(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404
	form = DoctorForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_doctor_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
	}
	return render(request, "sales/doctor_form.html", context)


def DoctorEdit(request, pk = None):
	instance = get_object_or_404(Doctor, pk = pk)
	form = DoctorForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user_id = request.user
		instance.save()
		pk_value = instance.pk
		return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s", "#id_doctor_id");</script>' % (pk_value, instance.name))
	context = {
		"form" : form,
	}
	return render(request, "sales/doctor_form.html", context)

def get_doctor_id(request):
	if not request.user.is_authenticated():
		raise Http404
	if request.is_ajax():
		doctor_name = request.GET['doctor_name']
		doctor_id = Doctor.objects.get(name = doctor_name).id
		data = {
			'doctor_id':str(doctor_id),
		}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")
