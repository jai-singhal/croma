from ..models import Unit
from .serializers import UnitApiSerialzer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser


class UnitListApiView(ListAPIView):
    queryset = Unit.objects.all().order_by('name')
    search_fields = ['name']
    serializer_class = UnitApiSerialzer
    permission_classes = (IsAdminUser,)

