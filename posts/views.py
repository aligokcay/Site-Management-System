from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Duyuru
from .forms import DuyuruForm

def is_admin(user):
    return user.is_superuser

@login_required
def duyuru_listesi(request):
    duyurular = Duyuru.objects.order_by('-created_at')
    return render(request, 'duyuru.html', {'duyurular': duyurular})

@user_passes_test(is_admin)
def duyuru_ekle(request):
    if request.method == 'POST':
        form = DuyuruForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('duyuru_listesi')
    else:
        form = DuyuruForm()

    return render(request, 'duyuru_ekle.html', {'form': form})
