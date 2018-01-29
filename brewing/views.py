from django.shortcuts import redirect, render, get_object_or_404
from .models import BrewingEvent


def batch_list(request):
    batches = BrewingEvent.objects.all()
    return render(request, 'packaging/batch_list.html', {'batches': batches})


def batch_detail(request, pk):
    batch = get_object_or_404(BrewingEvent, pk=pk)
    return render(request, 'packaging/batch_detail.html', {'batch': batch})    
