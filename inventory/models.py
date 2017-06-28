from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name='user')

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class CategoryEquipment(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class DeviceLocation(models.Model):
    room = models.CharField(max_length=50)
    wall_cabinet = models.CharField(max_length=50)
    shelf = models.PositiveSmallIntegerField()
    is_permanent = models.BooleanField(default=True)

    def __str__(self):
        return '%s , %s, %s' % (self.room, self.wall_cabinet, str(self.shelf))


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    location = models.ForeignKey(DeviceLocation, null=True)
    category = models.ForeignKey(CategoryEquipment, default='')
    equipimage = models.ImageField(upload_to='pic_folder/', default='pic_folder/demo.jpg')
    usermanual = models.FileField(upload_to='pdf/%Y/%m/%d', default='')
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class DeviceUsage(models.Model):
    equipment = models.ForeignKey(Equipment)
    taken_by = models.ForeignKey(User)
    purpose = models.CharField(max_length=300)
    temp_location = models.CharField(max_length=300)
    date_taken = models.DateTimeField(default=timezone.now)
    date_returned = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return '[Equipment: %s]' % (self.equipment)


