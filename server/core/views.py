from django.shortcuts import render
from core.serializers import GarbageComplaintSerializer, RecyclingComplaintSerializer
from core.models import GarbageComplaint, RecyclingComplaint
from rest_framework import generics
# Create your views here.


class GarbageComplaintView(generics.ListAPIView):
    serializer_class = GarbageComplaintSerializer
    
    
    def get_queryset(self):
        latitude = self.kwargs['lat']
        longitude = self.kwargs['long']
        queryset = GarbageComplaint.objects.filter(latitude)

class RecyclingComplaintView(generics.ListAPIView):
    serializer_class = RecyclingComplaintSerializer
    queryset = RecyclingComplaint.objects.all()

