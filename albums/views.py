from rest_framework import viewsets

from .models import Album
# Create your views here.
class AlbumViewSet(viewsets.ViewSet):
    queryset = Album.objects.all()