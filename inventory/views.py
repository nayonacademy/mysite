from datetime import timezone, date, datetime

from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.views.generic.base import View

from inventory.models import Equipment
from inventory.models import DeviceUsage
from inventory.forms import UsageForm
from django.utils import timezone

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
        user = User.objects.all()
        context = {
            'equipment': equipment,
            'user': user
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
        reverrselist = DeviceUsage.objects.filter(date_returned__isnull=True)
        context = {
            'my_reservations': reverrselist
        }
        return render(request, 'showreservation.html', context)


def equipmentReturn(request,pk):
    if request.method == 'GET':
        equip = DeviceUsage.objects.filter(pk=pk).get()
        DeviceUsage.objects.filter(pk=pk).update(date_returned=timezone.now())
        Equipment.objects.filter(id=equip.equipment_id).update(status=1)
        return HttpResponseRedirect(reverse('my_equipments'))


