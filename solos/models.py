from django.db import models
from albums.models import Album, Track
# Create your models here.


class Solo(models.Model):
    track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True)
    artist = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)
    # album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    slug = models.SlugField()

    class Meta:
        ordering = 'track', 'start_time'

    def get_duration(self):
        if self.start_time and self.end_time:
            return f'{self.start_time}-{self.end_time}'
        return ''

    def get_absolute_url(self):
        from django.urls import reverse

        # solo_detail_view must be added in urls as name
        return reverse('solo_detail_view', kwargs={
            'album': self.track.album.slug,
            'track': self.track.slug,
            'artist': self.slug,
        })
