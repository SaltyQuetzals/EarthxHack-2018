from django.shortcuts import get_object_or_404, render
from rest_framework import generics

from core.models import CouncilMember, GarbageComplaint, RecyclingComplaint
from core.serializers import (CouncilMemberSerializer,
                              GarbageComplaintSerializer,
                              RecyclingComplaintSerializer)

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


class CouncilMemberView(generics.RetrieveAPIView):
    """
    Retrieves the district whose number matches the
    query provided.
    """
    serializer_class = CouncilMemberSerializer
    queryset = CouncilMember.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            'district': self.kwargs['district_num']
        }
        return get_object_or_404(queryset, **filter)
