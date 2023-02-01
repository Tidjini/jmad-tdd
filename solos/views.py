from django.shortcuts import render
from .models import Solo
# Create your views here.


def index(request):
    solos_queryset = Solo.objects.all()

    if request.GET.get('instrument', None):
        solos_queryset = solos_queryset.filter(
            instrument=request.GET.get('instrument', None)
        )

    if request.GET.get('artist', None):
        solos_queryset = solos_queryset.filter(
            artist=request.GET.get('artist', None)
        )

    context = {'solos': solos_queryset}
    return render(request, 'solos/index.html', context)
