from ..models import (
					  Chain,
					  Company, 
					  Supplier
					)
from .serializers import (	
							ChainApiSerialzer, 
							CompanyApiSerialzer, 
							SupplierApiSerialzer
						 )
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class ChainListApiView(ListAPIView):
    queryset = Chain.objects.all().order_by('name')
    search_fields = ['name']
    serializer_class = ChainApiSerialzer
    permission_classes = (IsAuthenticated,)


class CompanyListApiView(ListAPIView):
    queryset = Company.objects.all().order_by('name')
    search_fields = ['name']
    serializer_class = CompanyApiSerialzer
    permission_classes = (IsAuthenticated,)


class SupplierListApiView(ListAPIView):
	queryset = Supplier.objects.all().order_by('name')
	search_fields = ['name']
	serializer_class = SupplierApiSerialzer
	permission_classes = (IsAuthenticated,)