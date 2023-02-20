from rest_framework import serializers

from .models import Solo


class SoloSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Solo
        fields = '__all__'
        read_only_fields = 'id',
