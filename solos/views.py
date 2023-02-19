from django.shortcuts import render


from .models import Solo

# Create your views here.


def index(request):
    solos_queryset = Solo.objects.all()
    artist_kwarg = request.GET.get('artist', None)

    if artist_kwarg:
        solos_queryset = solos_queryset.filter(artist=artist_kwarg)

    context = {'solos': solos_queryset}

    if context['solos'].count() == 0 and artist_kwarg:
        context['solos'] = Solo.get_artist_tracks_from_musicbrainz(
            artist_kwarg)

    import pdb
    pdb.set_trace()

    return render(request, 'solos/index.html', context)


# class SoloDetailView(DetailView):
#     model = Solo

def solo_detail(request, album, track, artist):
    context = {'solo': Solo.objects.get(
        slug=artist,
        track__slug=track,
        track__album__slug=album
    )}
    return render(request, 'solos/solo_detail.html', context)
