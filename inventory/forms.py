from django import forms
from inventory.models import DeviceUsage


class UsageForm(forms.ModelForm):
    class Meta:
        model = DeviceUsage
        fields = '__all__'


