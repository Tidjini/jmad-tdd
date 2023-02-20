from rest_framework import viewsets, mixins

from .models import Album
# Create your views here.


class AlbumViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Album.objects.all()
