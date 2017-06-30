from datetime import timezone, date, datetime
import json
from django.contrib.auth.models import User, Group
from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.views.generic.base import View
import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import Equipment
from inventory.models import DeviceUsage
from inventory.forms import UsageForm
from django.utils import timezone
from datetime import timedelta
from django.core import serializers
from rest_framework import viewsets
from .serializers import *

def home(request):
    return render(request, 'home.html')

def save(request):
    return render(request, 'save.html')

def my_equipments(request):
    my_equipments = Equipment.objects.all()
    return render(request, 'equipments.html', {'my_equipments': my_equipments})

def my_reservations(request):
    my_reservations = DeviceUsage.objects.order_by('-id')
    return render(request, 'reservations.html', {'my_reservations': my_reservations})

def my_usage(request):
    if request.method == 'POST':
        form = UsageForm(request.POST)
        if form.is_valid():
            deviceusage = form.save(commit=False)
            deviceusage.taken_by = request.user
            deviceusage.save()
            return redirect('save')         	
    else:
        form = UsageForm
    return render(request, 'usage.html', {'form': form})

def usage_edit(request,pk):
    deviceusage = get_object_or_404(DeviceUsage, pk=pk)
    if request.method == 'POST':
        form = UsageForm(request.POST,instance=deviceusage)
        if form.is_valid():
            deviceusage = form.save(commit=False)
            deviceusage.taken_by = request.user
            deviceusage.save()
            return redirect('save')          
    else:
        form = UsageForm(instance=deviceusage)
    return render(request, 'usage.html', {'form': form})


class BookingCalender(View):

    template_name = 'bookingcalender.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        equipment = Equipment.objects.filter(pk=pk)
        booking = DeviceUsage.objects.filter(equipment=pk)
        user = User.objects.all()
        context = {
            'equipment': equipment,
            'user': user,
        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('taken_by')
        # int(user_id)
        # user = User.objects.filter(id = user_id).get()
        print("User ID",user_id)
        purpose = request.POST.get('purpose')
        temp_location = request.POST.get('temp_location')
        equipment_id = request.POST.get('equipment')

        DeviceUsage.objects.create(purpose=purpose,temp_location=temp_location,equipment_id=equipment_id,taken_by_id=user_id)
        Equipment.objects.filter(id=equipment_id).update(status=0)
        return HttpResponseRedirect(reverse('my_equipments'))


def reservedequipment(request):
    if request.method == 'GET':
        reverrselist = DeviceUsage.objects.filter(end__isnull=True, taken_by=request.user.pk)
        context = {
            'my_reservations': reverrselist
        }
        return render(request, 'showreservation.html', context)


def equipmentReturn(request,pk):
    if request.method == 'GET':
        equip = DeviceUsage.objects.filter(pk=pk).get()
        DeviceUsage.objects.filter(pk=pk).update(end=datetime.datetime.now())
        Equipment.objects.filter(id=equip.equipment_id).update(status=1)
        return HttpResponseRedirect(reverse('my_equipments'))


def calculation(request):
    if request.method == 'POST':
        equipid = request.POST.get('equipid')
        cal = DeviceUsage.objects.filter(taken_by=request.user.pk, equipment=equipid)
        count = 0
        for i in cal:
            caltime = i.end - i.start
            newcal = divmod(caltime.days * 86400 + caltime.seconds, 60)
            print(newcal[0])
            count +=newcal[0]
        totaltime = str(timedelta(minutes=count))[:-3]

        return render(request, 'calculation.html', {'cal': cal, 'totaltime': totaltime})
    else:
        equip = Equipment.objects.all()
    return render(request, 'select_equipments.html', {'equip':equip})


def jsondataget(request):
    if request.method == "GET":
        return render(request, 'events.json')


# REST API SECTION
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DeviceUsageAPI(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None, *args, **kwargs):
        pk = self.kwargs['pk']
        client = DeviceUsage.objects.filter(equipment=pk)
        serializer = DeviceUsageSerializer(client, many=True)
        print(serializer)
        return Response(serializer.data)