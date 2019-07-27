from ..models import Party, Doctor
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser


class PartyListApiView(ListAPIView):
    queryset = Party.objects.all().order_by('name')
    search_fields = ['name']
    serializer_class = PartyApiSerialzer
    permission_classes = (IsAdminUser,)

class DoctorListApiView(ListAPIView):
    queryset = Doctor.objects.all().order_by('name')
    search_fields = ['name']
    serializer_class = DoctorApiSerialzer
    permission_classes = (IsAdminUser,)