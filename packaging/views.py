from django.shortcuts import render, get_object_or_404
from packaging.models import PackagingEvent, BrewingEvent

# Create your views here.


def home_page(request):
    return render(request, 'packaging/base.html')


def batch_list(request):
    batches = BrewingEvent.objects.all()
    return render(request, 'packaging/batch_list.html', {'batches': batches})


def batch_detail(request, pk):
    batch = get_object_or_404(BrewingEvent, pk=pk)
    return render(request, 'packaging/batch_detail.html', {'batch': batch})    


def packaging_list(request):
    packoffs = PackagingEvent.objects.all()
    return render(request, 'packaging/packaging_list.html', {'packoffs': packoffs})


def packoff_detail(request, pk):
    packoff = get_object_or_404(PackagingEvent, pk=pk)
    return render(request, 'packaging/packoff_detail.html', {'packoff': packoff})
