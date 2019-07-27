from ..models import Salt
from .serializers import SaltApiSerialzer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser


class SaltListApiView(ListAPIView):
    queryset = Salt.objects.all().order_by('name')
    search_fields = ['name']
    serializer_class = SaltApiSerialzer
    permission_classes = (IsAdminUser,)

