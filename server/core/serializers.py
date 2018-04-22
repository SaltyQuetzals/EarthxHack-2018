from rest_framework import serializers
from core.models import District, CouncilMember, RecyclingComplaint, GarbageComplaint


class CouncilMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilMember
        fields = ('name', 'email')


class RecyclingComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingComplaint
        fields = ('created_date', 'closed_date', 'latitude', 'longitude', 'score')


class GarbageComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarbageComplaint
        fields = ('created_date', 'closed_date', 'latitude', 'longitude', 'score')


class DistrictSerializer(serializers.ModelSerializer):
    council_member = CouncilMemberSerializer(many=False, read_only=True)
    garbage_complaints = GarbageComplaintSerializer(many=True, read_only=True)
    recycling_complaints = RecyclingComplaintSerializer(
        many=True, read_only=True)

    class Meta:
        model = District
        fields = ('number', 'area', 'population', 'council_member',
                  'recycling_complaints', 'garbage_complaints')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            'council_member', 'garbage_complaints', 'recycling_complaints')
        return queryset
