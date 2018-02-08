from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PackForm
from .models import PackagingEvent


# Create your views here.


# def home_page(request):
#     return render(request, 'packaging/base.html')


def packaging_list(request):
    packoffs = PackagingEvent.objects.all()
    return render(request, 'packaging/packaging_list.html', {'packoffs': packoffs})


def packoff_detail(request, pk):
    packoff = get_object_or_404(PackagingEvent, pk=pk)
    return render(request, 'packaging/packoff_detail.html', {'packoff': packoff})

@login_required
def packoff_new(request):
    if request.method == "POST":
        form = PackForm(request.POST)
        if form.is_valid():
            packoff = form.save()
            packoff.save()
            return redirect('packoff_detail', pk=packoff.pk)
    else:
        form = PackForm()
    return render(request, 'packaging/packoff_edit.html', {'form': form})

@login_required
def packoff_edit(request, pk):
    packoff = get_object_or_404(PackagingEvent, pk=pk)
    if request.method == "POST":
        form = PackForm(request.POST, instance=packoff)
        if form.is_valid():
            packoff = form.save()
            packoff.save()
            return redirect('packoff_detail', pk=packoff.pk)
    else:
        form = PackForm(instance=packoff)
    return render(request, 'packaging/packoff_edit.html', {'form': form})
