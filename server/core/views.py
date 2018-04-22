from django.shortcuts import render
from core.serializers import GarbageComplaintSerializer, RecyclingComplaintSerializer
from core.models import GarbageComplaint, RecyclingComplaint
from rest_framework import generics
# Create your views here.


class GarbageComplaintView(generics.ListAPIView):
    """
    Collects and returns all of the garbage 
    complaints that have occurred within a 
    2-mile radius.
    """
    serializer_class = GarbageComplaintSerializer

    def get_queryset(self):
        longitude = self.kwargs['long']
        latitude = self.kwargs['lat']
        return GarbageComplaint.objects.close_proximity(latitude, longitude)


class RecyclingComplaintView(generics.ListAPIView):
    """
    Collects and returns all of the recycling 
    complaints that have occurred within a 
    2-mile radius.
    """
    serializer_class = RecyclingComplaintSerializer
    queryset = RecyclingComplaint.objects.all()

    def get_queryset(self):
        longitude = self.kwargs['long']
        latitude = self.kwargs['lat']
        return RecyclingComplaint.objects.close_proximity(latitude, longitude)
