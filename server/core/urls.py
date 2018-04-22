from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
import core.views

urlpatterns = [
    url(r'garbage/(?P<lat>.+)/(?P<long>.+)/$',
        core.views.GarbageComplaintView.as_view()),
    url(r'recycling/(?P<lat>.+)/(?P<long>.+)/$',
        core.views.RecyclingComplaintView.as_view()),
    url(r'councilmembers/(?P<district_num>.+)/$',
        core.views.CouncilMemberView.as_view())
]
