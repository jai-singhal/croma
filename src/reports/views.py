from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.db.models import Count, Min, Sum, Avg, Max, When, DecimalField, Case, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import TruncMonth, TruncDay
from django.core.urlresolvers import resolve
from datetime import timedelta, date, datetime
import xlwt
from .forms import (
		InvoiceStatementForm,
		ItemWiseReportForm,
		ItemSupplierWiseReportForm,
		ExpiryReport,
		InventoryReport
	)
from accounts.models import YearEnding
from sales.models import SalesInvHrd, SalesInvDtl
from purchase.models import PurchaseInvHrd, PurchaseInvDtl
from item_master.models import Item
from company_master.models import Supplier, Company
from unit_master.models import Unit
from salt_master.models import Salt


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


class InvoiceStatementCreate(View):
	login_url = '/account/login/'
	template_name = 'reports/get_form.html'
	form_class = InvoiceStatementForm

	def get(self, request):
		session_id = request.session['session']
		current_url = resolve(request.path_info).url_name
		if current_url == "SalesInvSt":		title = "Sales Invoice Statement"
		elif current_url == "PurInvSt":		title = "Purchase Invoice Statement"
		InvStForm = self.form_class(request.POST or None, session_id = session_id)
		context = {
			"form" : InvStForm,
			"title": title
		}
		return render(self.request, self.template_name, context)

	def post(self, request):
		session_id = request.session['session']
		form = self.form_class(request.POST, session_id = session_id)
		if form.is_valid():
			to_dt = form.cleaned_data['to_dt']
			from_dt = form.cleaned_data['from_dt']
			current_url = resolve(request.path_info).url_name
			if current_url == "SalesInvSt":		url = "sales"
			elif current_url == "PurInvSt":		url = "purchase"

			return HttpResponseRedirect("/reports/" + url +"/InvoiceStatement/" + str(from_dt) +  "/" + str(to_dt))


def InvoiceStatementDetail(request, from_dt, to_dt):
	session_id = request.session['session']
	year_ending_obj = get_object_or_404(YearEnding, id = session_id)

	current_url = resolve(request.path_info).url_name

	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')

	report = []
	if current_url == "SalesInvSt_rep":
		for dt in daterange(start_date, end_date):

			query = SalesInvHrd.objects.filter(session_id =  year_ending_obj, \
				doc_dt = dt, doc_dt__gte = from_dt, doc_dt__lte = to_dt)
			if len(query):
				net_amount = query.aggregate(Sum("net_amount"))
				report.append([query, net_amount, dt])

		inv_type = "sales"
		title = "Sales Invoice Report"

	elif current_url == "PurInvSt_rep":
		for dt in daterange(start_date, end_date):
			query = PurchaseInvHrd.objects.filter(session_id =  year_ending_obj,  \
				doc_dt = dt, doc_dt__gte = from_dt, doc_dt__lte = to_dt)
			if len(query):
				paid_amount = query.aggregate(Sum("paid_amount"))
				report.append([query, paid_amount, dt])
		inv_type = "purchase"
		title = "Purchase Invoice Report"
	paginator = Paginator(report, 10) #posts per page
	page = request.GET.get('page')
	try:
		report = paginator.page(page)
	except PageNotAnInteger:
		report = paginator.page(1)
	except EmptyPage:
		report = paginator.page(paginator.num_pages)

	context = {
		"report": report,
		"page":page,
		"from_dt":start_date,
		"to_dt":to_dt,
		"inv_type": inv_type,
		"title": title
	}
	return render(request, "reports/post_form.html", context)



def export_PurinvoiceSt_report(request, from_dt, to_dt):
	response = HttpResponse(content_type='application/ms-excel')
	filename = "purinvSt_report_{}_to_{}.xls".format(from_dt, to_dt)
	response['Content-Disposition'] = 'attachment; filename='+filename

	current_session = get_object_or_404(YearEnding, id=request.session['session'])
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)
	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')

	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True
	
	columns = ['Doc Date', "Supplier Name", "Inv No.", "GST IN", "CGST", "SGST", "Disc", "Amount"]
	query = PurchaseInvHrd.objects.filter(session_id =  year_ending_obj, 
						 doc_dt__gte = from_dt, doc_dt__lte = to_dt)

	for col_num in range(len(columns)):
	    ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()

	for q in query:
		row_num += 1
		ws.write(row_num, 0, str(q.doc_dt), font_style)
		ws.write(row_num, 1, str(q.supplier_id.name), font_style)
		ws.write(row_num, 2, str(q.supp_chal_no), font_style)
		ws.write(row_num, 3, str(q.supplier_id.gst_no), font_style)
		ws.write(row_num, 4, str(q.paid_cgst), font_style)
		ws.write(row_num, 5, str(q.paid_sgst), font_style)
		ws.write(row_num, 6, str(q.paid_discount), font_style)
		ws.write(row_num, 7, str(q.paid_amount), font_style)

	wb.save(response)
	return response





class DateWiseInvoiceReportCreate(View):
	login_url = '/account/login/'
	template_name = 'reports/get_form.html'
	form_class = InvoiceStatementForm

	def get(self, request):
		session_id = request.session['session']
		current_url = resolve(request.path_info).url_name
		current_session = get_object_or_404(YearEnding, id=request.session['session'])
		if current_url == "MonhlyInvSale":		title = "Monthly Sales Statement"
		elif current_url == "MonhlyInvPur":		title = "Monthly Purchase Statement"
		if current_url == "DateInvSale":		title = "Day wise Sales Statement"
		elif current_url == "DateInvPur":		title = "Day wise Purchase Statement"

		InvStForm = self.form_class(request.POST or None, session_id = session_id)
		context = {
			"form" : InvStForm,
			"title": title,
			"current_session": current_session,

		}
		return render(self.request, self.template_name, context)

	def post(self, request):
		session_id = request.session['session']
		form = self.form_class(request.POST, session_id = session_id)

		if form.is_valid():
			to_dt = form.cleaned_data['to_dt']
			from_dt = form.cleaned_data['from_dt']

			current_url = resolve(request.path_info).url_name

			if current_url == "MonhlyInvSale" :    	url = "sales/MonthlyInvoiceStatement/"
			elif current_url == "DateInvSale":		url = "sales/DayInvoiceStatement/"
			elif current_url == "MonhlyInvPur" :	url = "purchase/MonthlyInvoiceStatement/"
			elif current_url == "DateInvPur":		url = "purchase/DayInvoiceStatement/"

			return HttpResponseRedirect("/reports/" + url + str(from_dt) +  "/" + str(to_dt))


def DateWisePurchaseInvoiceReportDetail(request, from_dt, to_dt):
	session_id = request.session['session']
	current_session = get_object_or_404(YearEnding, id=request.session['session'])
	year_ending_obj = YearEnding.objects.get(id = session_id)
	start_date = datetime.strptime(from_dt, '%Y-%m-%d').date()
	end_date = datetime.strptime(to_dt, '%Y-%m-%d').date()
	current_url = resolve(request.path_info).url_name

	if current_url == "MonhlyInvPur_det":
		query = PurchaseInvHrd.objects.filter(session_id =  current_session, \
					doc_dt__gte = start_date, doc_dt__lte = end_date).annotate(month = TruncMonth('doc_dt')).\
					values('month').annotate(amt = Sum('paid_amount'), total_cgst  = Sum('paid_cgst'), \
					total_sgst  =  Sum('paid_sgst'), total_disc = Sum('paid_discount')).\
					values('month', 'amt',  'total_cgst', 'total_sgst', 'total_disc').order_by('month')
		total = query.aggregate(total_amt = Sum('amt'), totalCGST = Sum('total_cgst'),  \
				totalSGST = Sum('total_sgst'), totalDISC = Sum('total_disc'))

		title = "Monthly Purchase Statement"
		report_type = "month"

	elif current_url == "DateInvPur_det":
		query = PurchaseInvHrd.objects.filter(session_id =  current_session, \
			doc_dt__gte = start_date, doc_dt__lte = end_date).annotate(day = TruncDay('doc_dt'))\
				.values('day').annotate(amt = Sum('paid_amount'), total_cgst  = Sum('paid_cgst'), \
				total_sgst  =  Sum('paid_sgst'), total_disc = Sum('paid_discount')\
				).values('day', 'amt', 'total_cgst', 'total_sgst', 'total_disc').order_by('day')

		total = query.aggregate(total_amt = Sum('amt'), totalCGST = Sum('total_cgst'),  \
				totalSGST = Sum('total_sgst'), totalDISC = Sum('total_disc'))

		title = "Day wise Purchase Statement"
		report_type = "day"

	paginator = Paginator(query, 30) #posts per page
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	context = {
		"report_type": report_type,
		"report": query,
		"page": page,
		"total": total,
		"from_dt":start_date,
		"to_dt":end_date,
		"title": title,
		"current_session": current_session,
	}
	return render(request, "reports/post_report1.html", context)



def DateWiseSaleInvoiceReportDetail(request, from_dt, to_dt):
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)
	current_session = get_object_or_404(YearEnding, id=request.session['session'])
	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')
	current_url = resolve(request.path_info).url_name
	if current_url == "MonhlyInvSale_det":
		query = SalesInvHrd.objects.filter(session_id =  current_session, \
					doc_dt__gte = start_date, doc_dt__lte = end_date).annotate(month = TruncMonth('doc_dt')).\
					values('month').annotate(amt = Sum('net_amount')).values('month', 'amt').order_by('month')
		title = "Monthly Sales Statement"
		report_type = "month"
		total = query.aggregate(total_amt = Sum('amt'))
	elif current_url == "DateInvSale_det":
		query = SalesInvHrd.objects.filter(session_id =  current_session, \
					doc_dt__gte = from_dt, doc_dt__lte = to_dt).annotate(day = TruncDay('doc_dt')).values('day').\
					annotate(amt = Sum('net_amount')).values('day', 'amt').order_by('day')
		title = "Day wise Purchase Statement"
		report_type = "day"
		total = query.aggregate(total_amt = Sum('amt'))
	paginator = Paginator(query, 30) 
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	context = {
		"report_type": report_type,
		"report": query,
		"page": page,
		"total": total,
		"from_dt":start_date,
		"to_dt":end_date,
		"title": title,
		"current_session": current_session,
	}
	return render(request, "reports/post_report2.html", context)


def export_purchase_report(request, from_dt, to_dt):
	response = HttpResponse(content_type='application/ms-excel')
	filename = "pur_report_{}_to_{}.xls".format(from_dt, to_dt)
	response['Content-Disposition'] = 'attachment; filename='+filename

	current_url = resolve(request.path_info).url_name
	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')
	filename = current_url + str(from_dt) + "to" + str(to_dt) + ".xls"
	response['Content-Disposition'] = 'attachment; filename=' + str(filename)

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	if current_url == "PurMonthReport":
		columns = ['Month', 'Total CGST', 'Total SGST', 'Total Discount', 'Amount']
		query = PurchaseInvHrd.objects.filter(id__gte =  year_ending_obj.year_sale_id, \
					doc_dt__gte = from_dt, doc_dt__lte = to_dt).annotate(month = TruncMonth('doc_dt')).values('month').\
					annotate(amt = Sum('paid_amount'), total_cgst  = Sum('paid_cgst'), \
					total_sgst  =  Sum('paid_sgst'), total_disc = Sum('paid_discount')).\
					values('month', 'amt',  'total_cgst', 'total_sgst', 'total_disc').order_by('month')

		rows = query.values_list('month', 'total_cgst', 'total_sgst', 'total_disc', 'amt')

	elif current_url == "PurDayReport":
		columns = ['Date', 'Total CGST', 'Total SGST', 'Total Discount', 'Amount']
		query = PurchaseInvHrd.objects.filter(id__gte =  year_ending_obj.year_sale_id, \
					doc_dt__gte = from_dt, doc_dt__lte = to_dt).annotate(day = TruncDay('doc_dt'))\
					.values('day').annotate(amt = Sum('paid_amount'), total_cgst  = Sum('paid_cgst'), \
					total_sgst  =  Sum('paid_sgst'), total_disc = Sum('paid_discount')\
					).values('day', 'amt', 'total_cgst', 'total_sgst', 'total_disc').order_by('day')
		rows = query.values_list('day', 'total_cgst', 'total_sgst', 'total_disc', 'amt')

	total = query.aggregate(total_amt = Sum('paid_amount'), total_cgst = Sum('paid_cgst'),  \
				total_sgst = Sum('paid_sgst'), total_disc = Sum('paid_discount'))

	for col_num in range(len(columns)):
	    ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, str(row[col_num]), font_style)

	ws.write(row_num+1, 0, "Total", font_style)
	ws.write(row_num+1, 1, total['total_cgst'], font_style)
	ws.write(row_num+1, 2, total['total_sgst'], font_style)
	ws.write(row_num+1, 3, total['total_disc'], font_style)
	ws.write(row_num+1, 4, total['total_amt'], font_style)
	wb.save(response)
	return response


def export_sale_report(request, from_dt, to_dt):
	response = HttpResponse(content_type='application/ms-excel')
	filename = "sale_report_{}_to_{}.xls".format(from_dt, to_dt)
	response['Content-Disposition'] = 'attachment; filename='+filename

	current_url = resolve(request.path_info).url_name

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)
	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')

	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	if current_url == "SaleMonthReport":
		columns = ['Month', 'Amount']
		query = SalesInvHrd.objects.filter(id__gte =  year_ending_obj.year_sale_id, \
					doc_dt__gte = from_dt, doc_dt__lte = to_dt).\
					annotate(month = TruncMonth('doc_dt')).values('month').\
					annotate(amt = Sum('net_amount')).values('month', 'amt').order_by('month')

		rows = query.values_list('month', 'amt')

	elif current_url == "SaleDayReport":
		columns = ['Date', 'Amount']
		query = SalesInvHrd.objects.filter(id__gte =  year_ending_obj.year_sale_id, \
					doc_dt__gte = from_dt, doc_dt__lte = to_dt).annotate(day = TruncDay('doc_dt')).values('day').\
					annotate(amt = Sum('net_amount')).values('day', 'amt').order_by('day')
		rows = query.values_list('day', 'amt')

	total = query.aggregate(total_amt = Sum('net_amount'))

	for col_num in range(len(columns)):
	    ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, str(row[col_num]), font_style)

	ws.write(row_num+1, 0, "Total", font_style)
	ws.write(row_num+1, 1, total['total_amt'], font_style)
	wb.save(response)
	return response


class ItemWiseReport(View):
	login_url = '/account/login/'
	template_name = 'reports/item_wise_report.html'
	form_class = ItemWiseReportForm

	def get(self, request):
		session_id = request.session['session']
		current_url = resolve(request.path_info).url_name
		if current_url == "ItemWiseSale":		title = "Item wise Sales Report"
		elif current_url == "ItemWisePur":		title = "Item wise Purchase Report"
		InvStForm = self.form_class(request.POST or None)
		session = YearEnding.objects.get(id = session_id)
		context = {
			"form" : InvStForm,
			"title": title,
			"min_date": session.from_dt,
			"max_date": session.to_dt,
		}
		return render(self.request, self.template_name, context)

	def post(self, request):
		session_id = request.session['session']
		form = self.form_class(request.POST)

		if form.is_valid():
			to_dt = form.cleaned_data['to_dt']
			from_dt = form.cleaned_data['from_dt']
			item = form.cleaned_data['item']
			item_id = Item.objects.get(name = item).id

			current_url = resolve(request.path_info).url_name

			if current_url == "ItemWiseSale":		url = "sales"
			elif current_url == "ItemWisePur":		url = "purchase"

			return HttpResponseRedirect("/reports/" + url +"/ItemWiseReport/" + str(item_id) + "/" + str(from_dt) +  "/" + str(to_dt))
		return HttpResponse("Form Not Valid")


def ItemWiseReportDetail(request, item_id, from_dt, to_dt):
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)

	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')
	current_url = resolve(request.path_info).url_name
	if current_url == "item_wise_sale_det":
		query = SalesInvDtl.objects.filter(hrd_id__id__gte =  year_ending_obj.year_sale_id, \
			hrd_id__doc_dt__gte = from_dt, hrd_id__doc_dt__lte = to_dt, item_id = item_id)
		title = "Item wise Sales Statement"

	elif current_url == "item_wise_pur_det":
		query = PurchaseInvDtl.objects.filter(hrd_id__id__gte =  year_ending_obj.year_sale_id, \
			hrd_id__doc_dt__gte = from_dt, hrd_id__doc_dt__lte = to_dt, item_id = item_id)
		title = "Item wise Purchase Statement"

	paginator = Paginator(query, 40) #posts per page
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	item = Item.objects.get(id = item_id)
	context = {
		"report": query,
		"from_dt":from_dt,
		"to_dt":to_dt,
		"title": title,
		"item":item
	}
	return render(request, "reports/item_wise_report_det.html", context)



class ItemSupplierWiseReport(View):
	login_url = '/account/login/'
	template_name = 'reports/item_supp_wise_report.html'
	form_class = ItemSupplierWiseReportForm

	def get(self, request):
		session_id = request.session['session']
		current_url = resolve(request.path_info).url_name

		InvStForm = self.form_class(request.POST or None)
		session = YearEnding.objects.get(id = session_id)
		context = {
			"form" : InvStForm,
			"min_date": session.from_dt,
			"max_date": session.to_dt,
		}
		return render(self.request, self.template_name, context)


	def post(self, request):
		session_id = request.session['session']
		form = self.form_class(request.POST)

		if form.is_valid():
			to_dt = form.cleaned_data['to_dt']
			from_dt = form.cleaned_data['from_dt']
			item = form.cleaned_data['item']
			supplier = form.cleaned_data['supplier']
			item_id = Item.objects.get(name = item).id
			supp_id = Supplier.objects.get(name = supplier).id

			return HttpResponseRedirect("/reports/purchase/" + "SupplierItemWiseReport/" + \
					str(item_id) + "/" + str(supp_id) + "/" + str(from_dt) +  "/" + str(to_dt))



def ItemSupplierWiseReportDetail(request, item_id, supp_id, from_dt, to_dt):
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)
	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')

	item = Item.objects.get(id = item_id)
	item_id = item.id
	suppiler = Supplier.objects.get(id = supp_id)
	suppiler_id = suppiler.id

	query = PurchaseInvDtl.objects.filter(hrd_id__id__gte =  year_ending_obj.year_sale_id, \
		hrd_id__doc_dt__gte = from_dt, hrd_id__doc_dt__lte = to_dt, item_id = item_id, hrd_id__supplier_id = suppiler_id)

	paginator = Paginator(query, 30) #posts per page
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	context = {
		"report": query,
		"suppiler": suppiler,
		"from_dt":from_dt,
		"to_dt":to_dt,
		"item":item,
		"title": "Item/Supplier Report"
	}
	return render(request, "reports/item_wise_report_det.html", context)


class ExpiryReport(View):
	login_url = '/account/login/'
	template_name = 'reports/expiry_report.html'
	form_class = ExpiryReport

	def get(self, request):
		session_id = request.session['session']

		ExpForm = self.form_class(request.POST or None)
		session = YearEnding.objects.get(id = session_id)
		context = {
			"form" : ExpForm,
			"min_date": session.from_dt,
			"max_date": session.to_dt,
		}
		return render(self.request, self.template_name, context)

	def post(self, request):
		session_id = request.session['session']
		form = self.form_class(request.POST)

		if form.is_valid():
			to_dt = form.cleaned_data['to_dt']
			from_dt = form.cleaned_data['from_dt']
			item = form.cleaned_data['item']
			item_id = Item.objects.get(name = item).id

			current_url = resolve(request.path_info).url_name
			if current_url == "ItemWiseSale":		url = "sales"
			elif current_url == "ItemWisePur":		url = "purchase"

			return HttpResponseRedirect("/reports/" + url +"/ItemWiseReport/" + str(item_id) + "/" + str(from_dt) +  "/" + str(to_dt))
		return HttpResponse("Form Not Valid")

def ExpiryReportDetail(request, item_id, from_dt, to_dt):
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)

	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')
	current_url = resolve(request.path_info).url_name
	if current_url == "item_wise_sale_det":

		query = SalesInvDtl.objects.filter(hrd_id__id__gte =  year_ending_obj.year_sale_id, \
			hrd_id__doc_dt__gte = from_dt, hrd_id__doc_dt__lte = to_dt, item_id = item_id)
		title = "Item wise Sales Statement"

	elif current_url == "item_wise_pur_det":

		query = PurchaseInvDtl.objects.filter(hrd_id__id__gte =  year_ending_obj.year_sale_id, \
			hrd_id__doc_dt__gte = from_dt, hrd_id__doc_dt__lte = to_dt, item_id = item_id)
		title = "Item wise Purchase Statement"

	paginator = Paginator(query, 40) #posts per page
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	item = Item.objects.get(id = item_id)
	context = {
		"report": query,
		"from_dt":from_dt,
		"to_dt":to_dt,
		"title": title,
		"item":item
	}
	return render(request, "reports/item_wise_report_det.html", context)




class InventoryReportView(View):
	login_url = '/account/login/'
	template_name = 'reports/inventory_report.html'
	form_class = InventoryReport

	def get(self, request, *args, **kwargs):
		utype = kwargs.pop('u_type')
		session_id = request.session['session']

		inventoryForm = self.form_class(request.POST or None)
		session = YearEnding.objects.get(id = session_id)
		context = {
			"form" : inventoryForm,
			"min_date": session.from_dt,
			"max_date": session.to_dt,
			"type": utype,
		}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		utype = kwargs.pop('u_type')
		session_id = request.session['session']
		form = self.form_class(request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			try:
				if utype == "Company":
					obj = Company.objects.get(name = name).id
				elif utype == "Salt":
					obj = Salt.objects.get(name = name).id
				elif utype == "Unit":
					obj = Unit.objects.get(name = name).id
			except:
				return HttpResponse(utype + " not Valid")

			return HttpResponseRedirect("/reports/InventoryReport/" + str(utype) + "/" + str(obj))
		return HttpResponse("Form Not Valid")


def InventoryReportDetail(request, u_type, id):
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)

	if u_type == "Company":
		query = Item.objects.filter(company_id = id)
		q1 = Company.objects.get(id = id)
		title = "Company"

	elif u_type == "Salt":
		query = Item.objects.filter(salt_id = id)
		q1 = Salt.objects.get(id = id)
		title = "Salt"

	elif u_type == "Unit":
		query = Item.objects.filter(unit_id = id)
		q1 = Unit.objects.get(id = id)
		title = "Unit"

	query = query.order_by('name')
	paginator = Paginator(query, 100) #posts per page
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	context = {
		"q1": q1,
		"report": query,
		"title": title,
	}
	return render(request, "reports/inventory_report_det.html", context)



def SupplierWiseReportDetail(request, from_dt, to_dt):
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)

	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')
	current_url = resolve(request.path_info).url_name

	current_session = get_object_or_404(YearEnding, id=request.session['session'])
	query = PurchaseInvHrd.objects.filter(session_id = current_session, doc_dt__gte = from_dt,\
		 doc_dt__lte = to_dt).values("supplier_id__name", "supplier_id__gst_no")\
			.annotate(
				total_amt = Sum(Case(
					When(paid_amount__gt = 0, then = "paid_amount"),
						output_field = DecimalField()
					)
				),
				total_inv = Count(Case(
					When(paid_amount__gt = 0, then = 1),
						output_field = IntegerField()
					)
				)
			).order_by('supplier_id__name')

	paginator = Paginator(query, 40) #posts per page
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	context = {
		"report": query,
		"title": "Supplier Wise Report",
		"from_dt":from_dt,
		"to_dt":to_dt,

	}
	return render(request, "reports/supp_wise_report_det.html", context)



class SupplierWiseReport(View):
	login_url = '/account/login/'
	template_name = 'reports/get_form.html'
	form_class = InvoiceStatementForm

	def get(self, request):
		session_id = request.session['session']
		InvStForm = self.form_class(request.POST or None, session_id = session_id)
		session = YearEnding.objects.get(id = session_id)
		context = {
			"form" : InvStForm,
			"title": "Supplier Wise Report",
			"min_date": session.from_dt,
			"max_date": session.to_dt,
		}
		return render(self.request, self.template_name, context)


	def post(self, request):
		session_id = request.session['session']
		form = self.form_class(request.POST, session_id = session_id)
		if form.is_valid():
			to_dt = form.cleaned_data['to_dt']
			from_dt = form.cleaned_data['from_dt']

			return HttpResponseRedirect("/reports/purchase/SupplierWiseReport/" + str(from_dt) +  "/" + str(to_dt))


def export_supplier_wise_report(request, from_dt, to_dt):
	response = HttpResponse(content_type='application/ms-excel')
	filename = "sup_wise_report_{}_to_{}.xls".format(from_dt, to_dt)
	response['Content-Disposition'] = 'attachment; filename='+filename

	current_session = get_object_or_404(YearEnding, id=request.session['session'])
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')
	session_id = request.session['session']
	year_ending_obj = YearEnding.objects.get(id = session_id)
	start_date = datetime.strptime(from_dt, '%Y-%m-%d')
	end_date = datetime.strptime(to_dt, '%Y-%m-%d')

	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['From Date', "To Date", "Supplier Name", "GST IN", "Amount"]
	query = PurchaseInvHrd.objects.filter(session_id = current_session, doc_dt__gte = from_dt,\
		 doc_dt__lte = to_dt).values("supplier_id__name", "supplier_id__gst_no")\
			.annotate(
				total_amt = Sum(Case(
					When(paid_amount__gt = 0, then = "paid_amount"),
						output_field = DecimalField()
					)
				),
				total_inv = Count(Case(
					When(paid_amount__gt = 0, then = 1),
						output_field = IntegerField()
					)
				)
			).order_by('supplier_id__name')

	for col_num in range(len(columns)):
	    ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()

	for q in query:
		row_num += 1
		ws.write(row_num, 0, str(from_dt), font_style)
		ws.write(row_num, 1, str(to_dt), font_style)
		ws.write(row_num, 2, str(q["supplier_id__name"]), font_style)
		ws.write(row_num, 3, str(q["supplier_id__gst_no"]), font_style)
		ws.write(row_num, 4, str(q["total_amt"]), font_style)
	wb.save(response)
	return response

