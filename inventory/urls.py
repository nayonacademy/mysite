from django.conf.urls import url

from inventory.views import BookingCalender
from . import views

urlpatterns = [
   url(r'^Home/$', views.home, name='home'),
   url(r'^save/$', views.save, name='save'),
   url(r'^my_equipments/$', views.my_equipments, name='my_equipments'),
   url(r'^my_usage/$', views.my_usage, name='my_usage'),
   url(r'^my_reservations/$', views.my_reservations, name='my_reservations'),
   url(r'^reservedequipment/$', views.reservedequipment, name='reservedequipment'),
   url(r'^reservedequipment/(?P<pk>\d+)/$', views.equipmentReturn, name='equipmentReturn'),
   url(r'^my_reservations/(?P<pk>\d+)/$', views.usage_edit, name='usage_edit'),
   url(r'^booking_calender/(?P<pk>\d+)/$', BookingCalender.as_view(), name='booking_calender'),
]
