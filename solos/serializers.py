from rest_framework import serializers

from .models import Solo


class SoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solo
