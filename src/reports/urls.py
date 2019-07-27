from django.conf.urls import url, include
from .views import (
		InvoiceStatementCreate,
		InvoiceStatementDetail,
		export_PurinvoiceSt_report,
		DateWiseInvoiceReportCreate,
		DateWisePurchaseInvoiceReportDetail,
		DateWiseSaleInvoiceReportDetail,
		ItemWiseReport,
		ItemWiseReportDetail,
		ItemSupplierWiseReport,
		ItemSupplierWiseReportDetail,
		ExpiryReport,
		export_sale_report,
		export_purchase_report,
		InventoryReportView,
		InventoryReportDetail,
		SupplierWiseReport,
		SupplierWiseReportDetail,
		export_supplier_wise_report,
	)


urlpatterns = [
	url(r'^api/', include("reports.api.urls"), name = "reports-api"),

	url(r'^sales/InvoiceStatement$', InvoiceStatementCreate.as_view(), name = "SalesInvSt"),
	url(r'^sales/InvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})$', \
						 InvoiceStatementDetail, name = "SalesInvSt_rep"),

	url(r'^purchase/InvoiceStatement$', InvoiceStatementCreate.as_view(), name = "PurInvSt"),
	url(r'^purchase/InvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$', \
						 InvoiceStatementDetail, name = "PurInvSt_rep"),

	url(r'^purchase/InvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/export_report$', \
						 export_PurinvoiceSt_report, name = "export_PurinvoiceSt_report"),


	# Date wise Report [Month Wise]
	url(r'^sales/MonthlyInvoiceStatement$', DateWiseInvoiceReportCreate.as_view(), name = "MonhlyInvSale"),
	url(r'^sales/MonthlyInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$', \
						 DateWiseSaleInvoiceReportDetail, name = "MonhlyInvSale_det"),
	url(r'^purchase/MonthlyInvoiceStatement$', DateWiseInvoiceReportCreate.as_view(), name = "MonhlyInvPur"),
	url(r'^purchase/MonthlyInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$', \
						 DateWisePurchaseInvoiceReportDetail, name = "MonhlyInvPur_det"),

	# Date wise Report [Day Wise]
	url(r'^sales/DayInvoiceStatement$', DateWiseInvoiceReportCreate.as_view(), name = "DateInvSale"),
	url(r'^sales/DayInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$', \
						 DateWiseSaleInvoiceReportDetail, name = "DateInvSale_det"),
	url(r'^purchase/DayInvoiceStatement$', DateWiseInvoiceReportCreate.as_view(), name = "DateInvPur"),
	url(r'^purchase/DayInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$', \
						 DateWisePurchaseInvoiceReportDetail, name = "DateInvPur_det"),

	# export to xlsv
	url(r'^purchase/MonthlyInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/export_report$', \
						 export_purchase_report, name = "PurMonthReport"),
	url(r'^purchase/DayInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/export_report$', \
					 export_purchase_report, name = "PurDayReport"),
	url(r'^sales/MonthlyInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/export_report$', \
						 export_sale_report, name = "SaleMonthReport"),
	url(r'^sales/DayInvoiceStatement/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/export_report$', \
					 export_sale_report, name = "SaleDayReport"),


	#Item WISE report
	url(r'^sales/ItemWiseReport$', ItemWiseReport.as_view(), name = "ItemWiseSale"),
	url(r'^sales/ItemWiseReport/(?P<item_id>\d+)/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})$', \
						 ItemWiseReportDetail, name = "item_wise_sale_det"),

	url(r'^purchase/ItemWiseReport$', ItemWiseReport.as_view(), name = "ItemWisePur"),
	url(r'^purchase/ItemWiseReport/(?P<item_id>\d+)/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})$', \
						 ItemWiseReportDetail, name = "item_wise_pur_det"),


	url(r'^purchase/SupplierItemWiseReport$', ItemSupplierWiseReport.as_view(), name = "ItemSuppWisePur"),
	url(r'^purchase/SupplierItemWiseReport/(?P<item_id>\d+)/(?P<supp_id>\d+)/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})$', \
						 ItemSupplierWiseReportDetail, name = "item_supp_wise_pur_det"),


	# supplier wise report
	url(r'^purchase/SupplierWiseReport$', SupplierWiseReport.as_view(), name = "supplier_wise_report"),
	url(r'^purchase/SupplierWiseReport/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$', \
						 SupplierWiseReportDetail, name = "supplier_wise_report_det"),

	url(r'^purchase/SupplierWiseReport/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/export_report', \
					 export_supplier_wise_report, name = "export_supplier_wise_report"),



	url(r'^ExpiryReport$', ExpiryReport.as_view(), name = "exp_rep"),

	url(r'^InventoryReport/(?P<u_type>\w+)/$', InventoryReportView.as_view(), name = "inventory_report"),
	url(r'^InventoryReport/(?P<u_type>\w+)/(?P<id>\d+)/$', InventoryReportDetail, name = "inventory_report_det"),

]
