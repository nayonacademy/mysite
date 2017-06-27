from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   url(r'^Home/$', views.home, name='home'),
   url(r'^save/$', views.save, name='save'),
   url(r'^my_equipments/$', views.my_equipments, name='my_equipments'),
   url(r'^my_usage/$', views.my_usage, name='my_usage'),
   url(r'^my_reservations/$', views.my_reservations, name='my_reservations'),
   url(r'^my_reservations/(?P<pk>\d+)/$', views.usage_edit, name='usage_edit'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)