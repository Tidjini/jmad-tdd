from django.utils.text import slugify
from rest_framework import serializers

from .models import Solo


class SoloSerializer(serializers.HyperlinkedModelSerializer):

    def validate(self, data):
        data['slug'] = slugify(data['artist'])
        return data

    class Meta:
        model = Solo
        fields = '__all__'
        read_only_fields = 'slug', 'id'
