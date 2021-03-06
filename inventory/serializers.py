from django.contrib.auth.models import User, Group
from rest_framework import serializers

from inventory.models import DeviceUsage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class DeviceUsageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceUsage
        fields = ('title','start','end')

