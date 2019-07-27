from ..models import Item 
from .serializers import ItemApiSerialzer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from .pagination import MyPageNumberPagination



class ItemListApiView(ListAPIView):
	serializer_class = ItemApiSerialzer
	permission_classes = (IsAdminUser,)
	filter_backends = [SearchFilter,]
	search_fields = ['name', 'id']

	# pagination_class = MyPageNumberPagination

	def get_queryset(self, *args, **kwargs):
		queryset = Item.objects.all().order_by('name')
		query = self.request.GET.get('q')
		if query:
			queryset = queryset.filter(name__startswith = query)

		return queryset


		
# class ItemRetrieveApiView(RetrieveAPIView):
#     lookup_field = 'pk'
#     serializer_class = ItemApiSerialzer
#     pagination_class = PageNumberPagination
#     permission_classes = (IsAdminUser,)

# class ItemCreateApiView(CreateAPIView):
#     lookup_field = 'pk'
#     serializer_class = ItemApiSerialzer
#     pagination_class = PageNumberPagination
#     permission_classes = (IsAdminUser,)

# class ItemUpdateApiView(UpdateAPIView):
#     lookup_field = 'pk'
#     serializer_class = ItemApiSerialzer
#     pagination_class = PageNumberPagination
#     permission_classes = (IsAdminUser,)

# class ItemDeleteApiView(DestroyAPIView):
#     lookup_field = 'pk'
#     serializer_class = ItemApiSerialzer
#     pagination_class = PageNumberPagination
#     permission_classes = (IsAdminUser,)