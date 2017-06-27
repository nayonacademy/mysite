from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from django.shortcuts import redirect
from inventory.models import Equipment
from inventory.models import DeviceUsage
from inventory.forms import UsageForm


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


