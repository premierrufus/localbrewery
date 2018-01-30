from django.shortcuts import redirect, render, get_object_or_404
from .models import Account
from .forms import AccountForm


def accounts_list(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/accounts_list.html', {'accounts': accounts})


def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'accounts/account_detail.html', {'account': account})    


def account_new(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = AccountForm()
    return render(request, 'accounts/account_edit.html', {'form': form})


def account_edit(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save()
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounts/account_edit.html', {'form': form})