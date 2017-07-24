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
import datetime, time

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
        user = User.objects.filter(id=user_id).get()
        # int(user_id)
        # user = User.objects.filter(id = user_id).get()
        print("User ID",user_id)
        purpose = request.POST.get('purpose')
        temp_location = request.POST.get('temp_location')
        equipment_id = request.POST.get('equipment')
        start = request.POST.get('start')
        end = request.POST.get('end')
        print('start time:', start, 'end time:', end)
        DeviceUsage.objects.create(purpose=purpose,temp_location=temp_location,equipment_id=equipment_id,taken_by_id=user_id, start=start, end=end, title=user.username)
        Equipment.objects.filter(id=equipment_id).update(status=0)
        return HttpResponseRedirect(reverse('my_equipments'))


def reservedequipment(request):
    if request.method == 'GET':
        reverrselist = DeviceUsage.objects.filter(status=True, taken_by=request.user.pk)
        context = {
            'my_reservations': reverrselist
        }
        return render(request, 'showreservation.html', context)


def equipmentReturn(request,pk):
    if request.method == 'GET':
        equip = DeviceUsage.objects.filter(pk=pk).get()
        DeviceUsage.objects.filter(pk=pk).update(status=0)
        Equipment.objects.filter(id=equip.equipment_id).update(status=1)
        return HttpResponseRedirect(reverse('my_equipments'))


def calculation(request):
    if request.method == 'POST':
        equipid = request.POST.get('equipid')
        start = request.POST.get('start')
        end = request.POST.get('end')
        cal = DeviceUsage.objects.filter(equipment=equipid)
        start1 = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        start1 = time.mktime(start1.timetuple())

        end1 = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        end1 = time.mktime(end1.timetuple())

        # print('start time :: ',datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S"))
        count = 0
        for i in cal:
            start = time.mktime(i.start.timetuple())
            print('database start',start, 'input start',start1)
            end = time.mktime(i.end.timetuple())
            print('database end',end, 'input end', end1)
            # print('counsdfsdf',end - start)
            # if (start > start1):
            #     newstart = start1
            #     print("if newstart", newstart)
            # else:
            #     newstart = start
            #     print("else newstart", newstart)
            #
            # if (end < end1):
            #     newend = end
            #     print("if newend", newend)
            # else:
            #     newend = end1
            #     print("else newend", newend)

            # if(end < start1):
            #     newstart = 0
            # elif(start1 > start):
            #     newstart = start
            # elif(start < start1):
            #     newstart = start1
            #
            # newend = ''
            # if(end1 < start):
            #     newend = 0
            # elif(end1 > end):
            #     newend = end
            # elif(end1 < end):
            #     newend = end1


            # if(end1 < start) and (start1 < start):
            #     count += 0
            #     print("1",count)
            # elif(start1 < start) and (end1 > end):
            #     count += end - start
            #     print("2", count)
            # elif(start1 < start) and (end1 < end):
            #     count += end1 - start
            #     print("3", count)
            # else:
            #     print("nno get")

            # elif(start1 < start) and (end1 > end):
            #     count += end - start
            #     print("2",count)
            # elif(start1 < start) and (end1 < end):
            #     count += start -end1
            #     print("3",count)
            # elif(start1>start) and (end1 < end):
            #     count += end1 - start1
            #     print("4",count)
            # elif(start1 > start) and (end1 > end):
            #     count += end - start1
            #     print("5",count)
            newstart = 0
            newend = 0


            # if start1 < start:
            #     newstart = start
            #     print("1-")
            # elif end1 < start:
            #     newstart = 0
            #     print("2-")
            # elif start1 > start:
            #     newstart = start1
            #     print("3-")
            # elif end1 < start and start1 < start:
            #     newstart = 0
            #     newend = 0
            #     print("4-")
            #
            #
            # if end1 > end and start1 > end:
            #     newend = 0
            #     newstart = 0
            #     print("1")
            # elif end1 < end:
            #     newend = end1
            #     print("2")
            # elif end1 > end:
            #     newend = end
            #     print("3")

            if(start1 < start) and ( end1 < start):
                newstart = 0
                newend = 0
                
            if(start1 < start) and (end1 < start):
                newstart = 0
                newend = 0
            elif(start1 < start) and (end1>end):
                newstart = start
                newend = end
            elif(start1 < start) and (end1 < end):
                newstart = start
                newend = end1
            elif(start1 > start) and (end1 < end):
                newstart = start1
                newend = end1
            elif(start1 > start) and (end1 > end):
                newstart = start1
                newend = end
            elif(start1 > end) and (end1 > end):
                newstart = 0
                newend = 0

            print("newstart", newstart, "newend ", newend)
            durration = newend - newstart
            print("duration::", durration)
            count += durration
        # print(count)
        minutes = count / 60
        # print(minutes)
        hours = minutes / 60
        # print(hours)
        days = hours / 24
        # print(days)
        totaltime = str(timedelta(minutes=minutes))[:-3]

        return render(request, 'calculation.html', {'cal': cal, 'totaltime': totaltime})
    else:
        equip = Equipment.objects.all()
    return render(request, 'select_equipments.html', {'equip':equip})


def jsondataget(request):
    if request.method == "GET":
        return render(request, '')


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
        return Response(serializer.data)