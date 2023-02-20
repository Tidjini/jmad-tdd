from rest_framework import serializers

from .models import Solo


class SoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solo
        fields = '__all__'
        read_only_fields = 'id',
