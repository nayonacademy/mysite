from django.conf.urls import url, include
from rest_framework import routers

from inventory.views import *
from . import views
router = routers.DefaultRouter()


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^bank/(?P<pk>\d+)/$', DeviceUsageAPI.as_view(), name="booking_api"),
    # url(r'^bank/(?P<pk>[0-9]+)/$', api_views.BankDetail.as_view()),
]
