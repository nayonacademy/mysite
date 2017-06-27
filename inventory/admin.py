from django.contrib import admin
from .models import *

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    pass


class CategoryEquipmentAdmin(admin.ModelAdmin):
    pass


class DeviceLocationAdmin(admin.ModelAdmin):
    pass


class EquipmentAdmin(admin.ModelAdmin):
    pass


class DeviceUsageAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CategoryEquipment, CategoryEquipmentAdmin)
admin.site.register(DeviceLocation, DeviceLocationAdmin)
admin.site.register(DeviceUsage, DeviceUsageAdmin)
admin.site.register(Equipment, EquipmentAdmin)




