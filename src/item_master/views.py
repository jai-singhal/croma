from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.views.generic import UpdateView
from django.views import View
from django.db import transaction
import json
from datetime import datetime
import logging
import os
from django.conf import settings
from .models import Item, Batch
from .forms import ItemMasterForm, BatchForm
from .serializers import BatchSerialzer, ItemSerialzer
from salt_master.models import Salt
from unit_master.models import Unit
from company_master.models import Chain
from purchase.models import PurchaseInvDtl
from sales.models import SalesInvDtl
from accounts.models import YearEnding


logger = logging.getLogger(__name__)

class CreateItem(View, LoginRequiredMixin):
	template_name = 'item_master/index.html'
	login_url = '/account/login'

	@staticmethod
	def saveItemQty(item_obj, batches):
		total_strip, total_nos = 0, 0
		for batch in batches:
			strip, nos = int(batch.strip), int(batch.nos)
			total_strip += strip
			total_nos += nos
		item_obj.handle_ItemQty_Stock_OnAdd(total_strip, total_nos)
		return True

	def get(self, request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(self.login_url)
		current_session = get_object_or_404(
			YearEnding, id=request.session['session'])

		item_form = ItemMasterForm(request.POST or None)
		try:   prev_item= Item.objects.order_by('-id').first()
		except:	prev_item = None
		context = {
			"form" : item_form,
			'is_create': True,
			"prev":prev_item,
			"current_session": current_session,
		}
		return render(self.request, self.template_name, context)

	@transaction.atomic
	def post(self, request):
		try:
			if self.request.method == "POST" and self.request.is_ajax():
				json_dict = json.loads(request.body.decode('utf-8'))
				item_info, batches = json_dict['item'], json_dict['batches']
				for i, batch in enumerate(batches):
					if batch['deleted'] == 1:
						del batches[i]
					
				sid = transaction.savepoint()
				item_serializer_instance = ItemSerialzer(data=item_info)
				if item_serializer_instance.is_valid():
					item_instance = item_serializer_instance.save()
				else:
					errors = {
						"item_errors": item_serializer_instance.errors,
					}
					logger.error(errors['item_errors'])
					return JsonResponse(errors, status = 400)
				batch_serialzer_instance = BatchSerialzer(data = batches, 
															many = True, item_id = item_instance.id)
				if batch_serialzer_instance.is_valid():
					batch_intances = batch_serialzer_instance.save()
					CreateItem.saveItemQty(item_instance, batch_intances)
					transaction.savepoint_commit(sid)
				else:
					transaction.savepoint_rollback(sid)
					errors = {
						"batch_errors": batch_serialzer_instance.errors,
						"item_errors": item_serializer_instance.errors
					}
					logger.error(errors)
					return JsonResponse(errors, status = 400)
				response = {'url' : item_instance.get_absolute_url()}
				return JsonResponse(response, status = 200)
		except Exception as e:
			logger.error(str(e))
			return JsonResponse({"error": str(e)}, status=400)


def RetrieveItem(request, pk = None):
	datem = datetime(datetime.now().year, datetime.now().month, 1)
    	
	if not request.user.is_authenticated():
		return redirect('/account/login')
	
	current_session = get_object_or_404(YearEnding, id=request.session['session'])
	instance = get_object_or_404(Item, id = pk)
	
	batch_queryset = Batch.objects.filter(item_id=pk, expiry__gt = datem).order_by("-expiry")
	batch_data = serialize('json', batch_queryset)
	json_batch_data = json.loads(batch_data)
	batch_data_set = [batch['fields'] for batch in json_batch_data]
	batch_data_set = json.dumps(batch_data_set)
	item_form = ItemMasterForm(request.POST or None, instance=instance)
	try:
		next_item = Item.objects.filter(pk__gt=instance.id).order_by('pk').first()
	except:
		next_item = None
		logger.warning("No next item found")
	try:
		prev_item = Item.objects.filter(pk__lt=instance.id).order_by('-pk').first()
	except:
		prev_item = None
		logger.warning("No previous item found")
	context = {
			"is_retrieve":True,
			"instance": instance,
			"form" : item_form,
			"batch_data_set": batch_data_set,
			"prev": prev_item,
			"next":next_item,
			"current_session": current_session,
	}

	return render(request, "item_master/index.html", context)


class UpdateItem(UpdateView, LoginRequiredMixin):
	template_name = 'item_master/index.html'
	login_url = '/account/login'
	
	def get(self, request, pk = None):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(self.login_url)
		current_session = get_object_or_404(YearEnding, id=request.session['session'])
		#Get the Item Query
		datem = datetime(datetime.now().year, datetime.now().month, 1)

		try:
			instance = get_object_or_404(Item, id = pk)
			item_form = ItemMasterForm(request.POST or None, instance = instance)
			#Get the respective Batch Query
			batch_queryset = Batch.objects.filter(item_id=pk, expiry__gt = datem).order_by("-expiry")
			batch_data = serialize('json', batch_queryset)
			json_batch_data = json.loads(batch_data)
			batch_data_set = [batch['fields'] for batch in json_batch_data]
			batch_data_set = json.dumps(batch_data_set)
		except Exception as e:
			logger.error(str(e))
			return HttpResponse("Something went wrong")

		context = {
			'is_update': True,
			"instance": instance,
			"form" : item_form,
			"batch_data_set": batch_data_set,
			"current_session": current_session
		}
		return render(self.request, self.template_name, context)
				
	@transaction.atomic
	def post(self, request, pk = None):
		sid = transaction.savepoint()
		try:
			if self.request.method == "POST" and self.request.is_ajax():
				json_dict = json.loads( request.body.decode('utf-8'))
				item, batches = json_dict['item'], json_dict['batches']	#NEW UPDATED ITEM = #NEW BATCH DICT
				try:
					item_obj = Item.objects.get(pk = pk)	#GETTING THE ITEM FROM DB
				except Exception as e:
					errors = {'item_errors': "Error: No Item/Batch Object Found"}
					logger.error(str(e))
					return JsonResponse(errors, status = 400)

				for batch_obj in batches:
					if batch_obj['deleted'] == 1:
						try:
							batch_instance = Batch.objects.get(item_id = item_obj, batch_no = batch_obj['batch_no'])
							item_obj.handle_ItemQty_Stock_OnSub(batch_instance.strip, batch_instance.nos)
							batch_instance.delete()
						except Exception as e:
							logger.error(str(e))

					elif batch_obj['deleted'] == 0:
						strip_new, nos_new = int(batch_obj['strip']), int(batch_obj['nos'])

						#If batch Exists in Database
						if Batch.objects.filter(item_id = item_obj, batch_no = batch_obj['batch_no']).exists():
							batch_qs = Batch.objects.get(item_id = item_obj, batch_no = batch_obj['batch_no'])
							serializer_batch = BatchSerialzer(batch_qs, data=batch_obj, item_id =item_obj.id, many = False)
							strip_old, nos_old = batch_qs.strip, batch_qs.nos
							
							item_obj.handle_ItemQty_Stock_OnAdd(strip_new-strip_old, nos_new-nos_old)
							batch_qs.handle_BatchQty_Stock_OnAdd(strip_new-strip_old, nos_new-nos_old)

						else:	#CREATE THE NEW BATCH
							serializer_batch = BatchSerialzer(data = batch_obj, item_id =item_obj.id, many = False)
							item_obj.handle_ItemQty_Stock_OnAdd(strip_new, nos_new)

						if serializer_batch.is_valid(): #SAVE THE BATCH
							batch_obj = serializer_batch.save()
						else:
							errors= {"batch_error":serializer_batch.errors,}
							transaction.savepoint_rollback(sid)
							logger.error(errors)
							return JsonResponse(errors, status = 400)

				serializer_item = ItemSerialzer(item_obj, data=item)
				if serializer_item.is_valid():
					item = serializer_item.save()
					transaction.savepoint_commit(sid)
					response = {'url' : item.get_absolute_url(),}
					return JsonResponse(response, status = 200)
				else:
					errors = {'item_errors': serializer_item.errors,}
					transaction.savepoint_rollback(sid)
				logger.error(errors)
				return JsonResponse(errors, status = 400)

		except Exception as e:
			logger.error(str(e))
			transaction.savepoint_rollback(sid)
			return JsonResponse({"errors": "Something went wrong"}, status = 400)


def DeleteItem(request):
	if request.method == "POST" and request.is_ajax():
		json_dict = json.loads( request.body.decode('utf-8'))
		item_name = json_dict['item_name']
		errors = {}
		try:
			item_obj = Item.objects.get(name = item_name)
		except:
			errors['no_object'] = "Error: No Item Object Found in Database"
			response = {'status': 0, "errors": errors}
			logger.error(errors)
			return JsonResponse(response, status=400)

		last_obj = Item.objects.last()
		if last_obj != item_obj:
			errors['stock_item'] = "Error: This Item Cannot be Deleted. You have Stock of this Item"
			response = {'status': 0, "errors": errors}
			logger.error(errors)
			return JsonResponse(response, status=400)
			
		if PurchaseInvDtl.objects.filter(item_id = item_obj).exists() or \
				SalesInvDtl.objects.filter(item_id = item_obj).exists():
			errors['stock_item'] = "Error: This Item Cannot be Deleted. You have Stock of this Item"
			response = {'status': 0, "errors": errors}
			logger.error(errors)
			return JsonResponse(response, status=400)

		batch_qs = Batch.objects.filter(item_id = item_obj)
		for obj in batch_qs:
			obj.delete()
		try:
			next_item = Item.objects.get(id = item_obj.id + 1)
			url = next_pur_inv.get_absolute_url()
		except:
			next_item = None
			url = "/item/create"

		item_obj.delete()
		return JsonResponse({"status": 1, "url": url}, status = 200)
	logger.error({"errors": "Something went wrong"})
	return JsonResponse({"status": 0}, status = 400)



def search_item(request):
	if request.method == "GET" and request.is_ajax():
		item_q = request.GET['search_name']
		item_list = Item.objects.filter(name__startswith = item_q)
		if item_list.count() > 100:
			item_list = item_list[0:100]
		item_json_Arr = []
		for item in item_list:
			item_obj = {}
			item_obj['name'] = str(item.name)
			item_obj['url'] = str(item.get_absolute_url())
			item_json_Arr.append(item_obj)

		data = {
			"items_query": json.dumps(item_json_Arr), #serialize("json", item_json_Arr),
		}
		return JsonResponse(data, status = 200)

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

def get_item_batches(request):
	if request.method == "GET" and request.is_ajax():
		datem = datetime(datetime.now().year, datetime.now().month, 1)
    		
		print(datem)
		item_id = request.GET['item_id']
		batch_list = Batch.objects.filter(item_id = int(item_id), 
										expiry__gt = datem).order_by('expiry')

		item = Item.objects.get(id = item_id)
		item_json_Arr = {
					"item_code":item.item_code,
					"company":item.company_id.name,
					"salt": item.salt_id.name,
					"unit": item.unit_id.name,
					"unit_conv": item.unit_id.number,
					"strip_stock": int(item.strip_stock),
					"nos_stock": int(item.nos_stock),
					"cgst": float(item.cgst),
					"sgst": float(item.sgst),
				}

		batch_json_Arr = []
		for batch in batch_list:
			batch_obj = {}
			batch_obj['batch_no'] = str(batch.batch_no)
			batch_obj['expiry'] = batch.expiry.strftime("%Y-%m")
			batch_obj['strip'] = str(int(batch.strip))
			batch_obj['nos'] = str(int(batch.nos))
			batch_obj['strip_pur'] = str(batch.strip_pur)
			batch_obj['strip_sale'] = str(batch.strip_sale)
			batch_obj['mrp'] = str(batch.mrp)
			batch_obj['std_rt'] = str(batch.std_rt)
			batch_obj['inst_rt'] = str(batch.inst_rt)
			batch_obj['trade_rt'] = str(batch.trade_rt)
			batch_json_Arr.append(batch_obj)
		data = {
			"batch_query": json.dumps(batch_json_Arr, default=date_handler),
			"instance": json.dumps(item_json_Arr,  default=date_handler),
		}
		return JsonResponse(data, status = 200)


def search_item_info(request):
	if request.method == "GET" and request.is_ajax():
		item = request.GET['item_name']
		datem = datetime(datetime.now().year, datetime.now().month, 1)
		try:
			item_q = get_object_or_404(Item, name = item)
			
			batches = Batch.objects.filter(item_id = item_q, 
						expiry__gt = datem)
			response = {
				"status" : "1",
			 	"company" : item_q.company_id.name,
				"unit" : item_q.unit_id.name,
				"salt" : item_q.salt_id.name,
				"strip_stock": item_q.strip_stock,
				"nos_stock": item_q.nos_stock,
				"supplier": item_q.company_id.supp_id.name,
				"batches" : serialize("json", batches),
			}
			return JsonResponse(response, status = 200)
		except Exception as e:
			response = {"status" : "0"}
			logger.error(str(e))
			return JsonResponse(response, status = 400)


