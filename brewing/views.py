from django.shortcuts import redirect, render, get_object_or_404
from .forms import BatchForm
from .models import BrewingEvent


def batch_list(request):
    batches = BrewingEvent.objects.all()
    return render(request, 'brewing/batch_list.html', {'batches': batches})


def batch_detail(request, pk):
    batch = get_object_or_404(BrewingEvent, pk=pk)
    return render(request, 'brewing/batch_detail.html', {'batch': batch})    


def batch_new(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            batch.save()
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm()
    return render(request, 'brewing/batch_edit.html', {'form': form})


def batch_edit(request, pk):
    batch = get_object_or_404(BrewingEvent, pk=pk)
    if request.method == "POST":
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            batch = form.save()
            batch.save()
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm(instance=batch)
    return render(request, 'brewing/batch_edit.html', {'form': form})