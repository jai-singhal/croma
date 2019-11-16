from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import transaction
from django.views.generic import UpdateView
import json
import logging
import sys

from item_master.models import Item, Batch
from .models import *
from .forms import *
from .serializers import *
from .utils import create_PurchaseInvDtl_JSON_QuerySet

logger = logging.getLogger(__name__)



class CreatePurchase(View, LoginRequiredMixin):
	login_url = '/account/login/'
	template_name = 'purchase/index.html'
	def dispatch(self, *args, **kwargs):
		return super(CreatePurchase, self).dispatch(*args, **kwargs)

	def get(self, request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(self.login_url)
		PurInvHrdForm = PurchaseInvHrdForm(request.POST or None)
		PurInvDtlForm = PurchaseInvDtlForm(request.POST or None)

		current_session_id = request.session['session']
		current_session = get_object_or_404(YearEnding, id = current_session_id)

		try:
			prev_pur = PurchaseInvHrd.objects.filter(session_id=current_session).order_by('-id')[0]
			doc_no = prev_pur.doc_no + 1
		except Exception as e:
			prev_pur = None
			doc_no = 1
			logger.error(str(e))

		context = {
			"hrd_form" : PurInvHrdForm,
			"dtl_form" : PurInvDtlForm,
			"doc_no": doc_no,
			'is_create': True,
			"prev":prev_pur,
			"current_session":current_session
		}
		return render(self.request, self.template_name, context)

	# @transaction.atomic
	def post(self, request):
		if not request.user.is_authenticated():
			raise Http404
		try:
			with transaction.atomic():
				if self.request.method == "POST" and self.request.is_ajax():
					current_session_id = request.session['session']
					current_session = get_object_or_404(YearEnding, id = current_session_id)
					json_dict = json.loads( request.body.decode('utf-8'))
					pur_info, pur_items = json_dict['pur_info'], json_dict['item_table']
					for i, item in enumerate(pur_items):
						if item['deleted'] == 1:
							del pur_items[i]
					try:
						next_doc_no = PurchaseInvHrd.objects.filter(session_id=current_session).order_by('-id')[0].doc_no + 1
					except Exception as e:
						logger.error(str(e))
						next_doc_no = 1
					
					pur_info['session_id'], pur_info['doc_no'] = current_session_id, next_doc_no
					#saving Purchasehrd Form
					serializer_pur_hrd =  PurchaseInvHdrSerialzer(data=pur_info)
					if serializer_pur_hrd.is_valid():
						pur_hrd_obj = serializer_pur_hrd.save()
					else:
						logger.error(str(serializer_pur_hrd.errors))
						return JsonResponse({"error": serializer_pur_hrd.errors}, status=400)

					#Handling Item Table
					for item in pur_items:
						item_id = item['item_id']
						if Item.objects.filter(id = item_id).exists():
							item_obj = Item.objects.get(id = item_id)
							total_strip = int(item['strip_qty']) + int(item['strip_free'])
							total_nos = int(item['nos_qty']) + int(item['nos_free'])
							#Subtract from strip and nos stock of Item Database
							item_obj.handle_ItemQty_Stock_OnAdd(total_strip, total_nos)
							item_obj.handle_c_s_gst(item['cgst'], item['sgst'])
							# Adding a new batch if it is new, if not then increase the stcok of batch
							if Batch.objects.filter(item_id = item_obj, batch_no = item['batch_no']).exists():
								item_batch = Batch.objects.get(batch_no = item['batch_no'], item_id = item_obj)
								item_batch.handle_BatchQty_Stock_OnAdd(total_strip, total_nos)
							else:
								pur_rate = float(item['rate'])
								mrp = float(item['mrp'])
								try:
									item_batch = Batch.objects.create(item_id = item_obj,
																	batch_no = item['batch_no'], expiry = item['expiry'],
																	strip = int(item['strip_qty']) + int(item['strip_free']),
																	nos = int(item['nos_qty']) + int(item['nos_free']),
																	strip_pur = pur_rate, strip_sale = item['sales_rate'],
																	mrp = mrp, sale_rt = mrp*0.1, inst_rt = mrp,
																	trade_rt = item['trade_rate'],
																	std_rt = item['std_rate'],
																	pur_rt = pur_rate*0.1, conv = int(item['conv'])
																)
								except Exception as e:
									logger.error(str(e))
									return JsonResponse({"error": str(e)}, status = 400)

							#USE SERIALOIZER TO ADD NEW BATCH IN BATCH DB..
							serializer_pur_dtl = PurchaseInvDtlSerialzer(data=item)
							item["hrd_id"] = pur_hrd_obj.id
							if serializer_pur_dtl.is_valid():
								serializer_pur_dtl.save()
							else:
								response = {"error": str(serializer_pur_dtl.errors), "item_name": item_obj.name}
								return JsonResponse(response, status = 400)
						else:
							response = {'errors':"Item name '{}' is required".format(item["item_name"])}
							return JsonResponse(response, status=400)
					response = {
						'status': 1,
						'url' : pur_hrd_obj.get_absolute_url(),
					}
					return JsonResponse(response, status = 200)
		except Exception as e:
			logger.error("Error on line {} \nType: {} \nError:{}".format(sys.exc_info()[-1], type(e).__name__, str(e)))
			return JsonResponse({"error": str(e)}, status = 400)

@login_required
def RetrievePurchase(request, pk = None):
	if not request.user.is_authenticated():
		raise Http404
	current_session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id = current_session_id)

	PurInvDtlForm = PurchaseInvDtlForm(request.POST or None)
	#Get the sale inv Query
	purchaseInvhrd_query = get_object_or_404(PurchaseInvHrd, id = pk, session_id = current_session)
	doc_no = purchaseInvhrd_query.doc_no
	PurInvHrdForm = PurchaseInvHrdForm(request.POST or None, instance = purchaseInvhrd_query)

	#Get the respective Items Query
	PurInvDtl_queryset = PurchaseInvDtl.objects.filter(hrd_id = pk)	#Queryset of all items assocuadted with hrd_id = pk
	pur_dtl_item_arr = create_PurchaseInvDtl_JSON_QuerySet(PurInvDtl_queryset)	#create a dict of all sale item for respective invoice
	purDtl_item_set_json = json.dumps(pur_dtl_item_arr)	#get the json data for all items

	try:
		next_pur_inv = PurchaseInvHrd.objects.filter(id__gt = pk,session_id = current_session).order_by("pk")[0]
	except Exception as e:
		logger.warning(str(e))
		next_pur_inv = None
	try:
		prev_pur_inv = PurchaseInvHrd.objects.filter(id__lt = pk, session_id = current_session).order_by("-pk")[0]
	except Exception as e:
		logger.warning(str(e))
		prev_pur_inv = None

	context = {
			"is_retrieve":True,
			"saleDtl_item_set_json": purDtl_item_set_json,
			"doc_no": doc_no,
			"instance": purchaseInvhrd_query,
			"hrd_form" : PurInvHrdForm,
			"dtl_form" : PurInvDtlForm,
			"prev": prev_pur_inv,
			"next":next_pur_inv,
			"current_session":current_session
	}
	return render(request, 'purchase/index.html', context)


class UpdatePurchase(UpdateView, LoginRequiredMixin):
	template_name = 'purchase/index.html'
	def dispatch(self, *args, **kwargs):
		return super(UpdatePurchase, self).dispatch(*args, **kwargs)

	def get(self, request, pk = None):
		if not request.user.is_authenticated():
			raise Http404

		current_session_id = request.session['session']
		current_session = get_object_or_404(YearEnding, id = current_session_id)

		PurInvDtlForm = PurchaseInvDtlForm(request.POST or None)
		#Get the Purchase inv Query
		purchaseInvhrd_query = get_object_or_404(PurchaseInvHrd, id = pk)
		doc_no = purchaseInvhrd_query.doc_no

		PurInvHrdForm = PurchaseInvHrdForm(request.POST or None, instance = purchaseInvhrd_query)
		PurInvDtl_queryset = PurchaseInvDtl.objects.filter(hrd_id = pk)	#Queryset of all items assocuadted with hrd_id = pk
		pur_dtl_item_arr = create_PurchaseInvDtl_JSON_QuerySet(PurInvDtl_queryset)	#create a dict of all sale item for respective invoice
		purDtl_item_set_json = json.dumps(pur_dtl_item_arr)	#get the json data for all items

		context = {
				"is_update":True,
				"saleDtl_item_set_json": purDtl_item_set_json,
				"doc_no": doc_no,
				"instance": purchaseInvhrd_query,
				"hrd_form" : PurInvHrdForm,
				"dtl_form" : PurInvDtlForm,
				"current_session":current_session
		}
		return render(request, self.template_name, context)

	# @transaction.atomic
	def post(self, request, pk = None):
		# sid = transaction.savepoint()
		try:
			with transaction.atomic():
				if self.request.method == "POST" and self.request.is_ajax():
					#getting the jon array of saleinfo and sale_item_table_data
					json_dict = json.loads( request.body.decode('utf-8'))
					#taking off both form data
					pur_info, pur_items = json_dict['pur_info'], json_dict['item_table']
					pur_info["session_id"] = request.session['session']
					# errors = {}
					try:
						pur_info_obj = PurchaseInvHrd.objects.get(id = pk)	#Getting the object of sale info from Db
					except Exception as e:
						logger.error(str(e))
						return JsonResponse({"error": str(e)}, status=400)

					serializer_PurchaseInvHrd = PurchaseInvHdrSerialzer(pur_info_obj, data=pur_info)
					pur_hrd_save_status = False
					if serializer_PurchaseInvHrd.is_valid():
						pur_hrd_save_status = True
					else:
						logger.error((serializer_PurchaseInvHrd.errors))
						return JsonResponse({"error": serializer_PurchaseInvHrd.errors}, status=400)

					# Saving new item or update existing item
					# Handling Item Table. Changing The database according to new update: Create it or update it or delete it
					for item in pur_items:
						#Taking the Json array of item table(item one by one), gettig each item name and change it to its item_id
						item_id = item['item_id']
						item['hrd_id'] = pur_info_obj.id
						try:
							item_obj = Item.objects.get(id = item_id)
						except Exception as e:
							return JsonResponse({"error": str(e)}, status=400)

						#Delete the Item if not present or status of deleted is True
						if item['deleted'] == 1:	#If Item is not present in ## Delete the Item
							try:
								PurchaseInvItem_instance = PurchaseInvDtl.objects.get(hrd_id = pk, item_id = item_obj, batch_no = item['batch_no'])
								strip, nos = PurchaseInvItem_instance.strip_qty + PurchaseInvItem_instance.strip_free, PurchaseInvItem_instance.nos_qty + PurchaseInvItem_instance.nos_free

								PurchaseInvItem_instance.delete()
								item_obj.handle_ItemQty_Stock_OnSub(strip,nos)
								try:
									batch_instance = Batch.objects.get(item_id = item_obj, batch_no = item['batch_no'])
									batch_instance.handle_BatchQty_Stock_OnSub(strip,nos)
								except Exception as e:
									logger.error(str(e))
							except Exception as e:
								return JsonResponse({"error": str(e)}, status=400)

						elif item['deleted'] == 0:
							if Batch.objects.filter(item_id = item_obj, batch_no = item['batch_no']).exists():
								item_batch = Batch.objects.get(batch_no = item['batch_no'], item_id = item_obj)
							else:
								pur_rate, mrp = float(item['rate']), float(item['mrp'])
								try:
									item_batch = Batch.objects.create(item_id = item_obj,
																batch_no = item['batch_no'], expiry = item['expiry'],
																strip = 0 , nos = 0,
																strip_pur = pur_rate, strip_sale = item['sales_rate'],
																mrp = mrp, sale_rt = mrp*0.1, inst_rt = mrp,
																trade_rt = item['trade_rate'],
																std_rt = item['std_rate'],
																pur_rt = pur_rate*0.1, conv = int(item['conv'])
																)
								except Exception as e:
									logger.error(str(e))
									return JsonResponse({"error": str(e)}, status=400)

							total_strip_new, total_nos_new = int(item['strip_qty']) + int(item['strip_free']), int(item['nos_qty']) + int(item['nos_free'])
							item_obj.handle_c_s_gst(item['cgst'], item['sgst'])
							# UPDATE THE Existing BATCH
							
							if PurchaseInvDtl.objects.filter(hrd_id = pk, item_id = item['item_id'], batch_no = item['batch_no']).exists():
								#getting the entery from DB  of hrd_id= pk, batch_no = item's batch_no and item_id = item_obj
								item_qs = PurchaseInvDtl.objects.get(hrd_id = pk, item_id = item['item_id'], batch_no = item['batch_no'])
								total_strip_old, total_nos_old = item_qs.strip_qty + item_qs.strip_free, item_qs.nos_qty + item_qs.nos_free
								strip, nos = total_strip_new - total_strip_old, total_nos_new - total_nos_old
								#Increement the Stock Strip and Nos (New-old)
								item_obj.handle_ItemQty_Stock_OnAdd(strip, nos)
								item_batch.handle_BatchQty_Stock_OnAdd(strip, nos)
								#serialize the item
								serializer_item = PurchaseInvDtlSerialzer(item_qs, data=item)

							else:	# CREATE THE NEW BATCH
								serializer_item = PurchaseInvDtlSerialzer(data = item)
								#Addition from strip and nos stock of Item Database
								item_obj.handle_ItemQty_Stock_OnAdd(total_strip_new, total_nos_new)
								# Subtracting the qty [nos and strip] from batch Table
								item_batch.handle_BatchQty_Stock_OnAdd(total_strip_new, total_nos_new)

							item["hrd_id"] = pur_info_obj.id
							if serializer_item.is_valid(): #SAVE THE NEW OR UPDATE ITEM
								serializer_item.save(hrd_id = pur_info_obj)
							else:
								logger.error(str(serializer_item.errors))
								return JsonResponse({"error": str(serializer_item.errors)}, status=400)

					if pur_hrd_save_status:
						PurchaseInvHrd_instance = serializer_PurchaseInvHrd.save()

					response = {
							'status': 1,
							'message': "Successfully Saved",
							'url' : PurchaseInvHrd_instance.get_absolute_url(),
					}
					# transaction.savepoint_commit(sid)
					return JsonResponse(response, status=200)
		except Exception as e:
			logger.error("Error on line {} \nType: {} \nError:{}".format(sys.exc_info()[-1], type(e).__name__, str(e)))
			# transaction.savepoint_rollback(sid)
			response = {"error": str(e)}
			return JsonResponse(response, status=400)


def DeletePurchase(request):
	current_session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id = current_session_id)

	if request.method == "POST" and request.is_ajax():

		json_dict = json.loads( request.body.decode('utf-8'))
		doc_no = json_dict['doc_no']

		try:
			pur_inv_obj = PurchaseInvHrd.objects.get( session_id = current_session, doc_no = int(doc_no))
		except Exception as e:
			return JsonResponse({"error": str(e)}, status = 400)

		last_obj = PurchaseInvHrd.objects.last()
		if last_obj != pur_inv_obj:
			return JsonResponse({"error": "Error: You cannot delete this Invoice"}, status = 400)

		pur_dtl_qs = PurchaseInvDtl.objects.filter(hrd_id = pur_inv_obj)
		for obj in pur_dtl_qs:
			try:
				item_obj = Item.objects.get(id = obj.item_id.id)
				batch_obj = Batch.objects.get(item_id = item_obj, batch_no = obj.batch_no)
				batch_obj.handle_BatchQty_Stock_OnSub(obj.strip_qty + obj.strip_free, obj.nos_qty + obj.nos_free)
				item_obj.handle_ItemQty_Stock_OnSub(obj.strip_qty + obj.strip_free, obj.nos_qty + obj.nos_free)
			except Exception as e:
				continue

			obj.delete()

		try:
			next_pur_inv = PurchaseInvHrd.objects.filter(id__gt = pur_inv_obj.id, session_id = current_session).order_by("pk")[0]
			url = next_pur_inv.get_absolute_url()
		except Exception as e:
			next_sale_inv = None
			url = "/purchase/create"

		pur_inv_obj.delete()
		return JsonResponse({"url": url}, status=200)

	return JsonResponse({"status": 0}, status=400)



def SearchInv(request):
	current_session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id = current_session_id)

	if request.method == "GET" and request.is_ajax():
		inv_no = request.GET.get("pur_inv")
		if PurchaseInvHrd.objects.filter(session_id = current_session, doc_no = inv_no).exists():
			purchase_inv_obj = PurchaseInvHrd.objects.get(session_id = current_session, doc_no = inv_no)
			response = {"status": 1, "msg" : purchase_inv_obj.get_absolute_url()}
		else:
			response = {"status": 0, "msg": "No Invoice Found"}

	return JsonResponse(response, status=200)


def checkSupplierNameInv(request):
	try:
		current_session_id = request.session['session']
		current_session = get_object_or_404(YearEnding, id = current_session_id)
		if request.method == "POST" and request.is_ajax():
			json_dict = json.loads(request.body.decode('utf-8'))
			inv_no = json_dict['challanNo']
			name = json_dict['supplierName']
			supp_id = Supplier.objects.get(name = name).id
			if PurchaseInvHrd.objects.filter(session_id=current_session, 
									supp_chal_no=inv_no, supplier_id=supp_id).exists():
				response = {"status": 0}
				return JsonResponse(response, status=400)
			else:
				response = {"status": 1}
				return JsonResponse(response, status = 200)

	except Exception as e:
		response = {"status": str(e)}
		return JsonResponse(response, status=400)	
