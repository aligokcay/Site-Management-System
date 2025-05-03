from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Duyuru, IstekSikayet
from django.http import HttpResponseForbidden
from .forms import DuyuruForm, IstekSikayetForm

def is_admin(user):
    return user.is_superuser

def duyuru_listesi(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Sadece başlık ve içerik kaydedeceğiz
        Duyuru.objects.create(title=title, content=content)

        return redirect('duyuru_listesi')  # Başarılı olunca tekrar listeye yönlendir
    
    # GET isteği için duyuruları çekelim
    duyurular = Duyuru.objects.all()
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

def duyuru_k(request):
    duyurular = Duyuru.objects.all()
    return render(request, 'duyuru_k.html', {'duyurular': duyurular})

def duyuru_p(request):
    duyurular = Duyuru.objects.all()
    return render(request, 'duyuru_p.html', {'duyurular': duyurular})

@login_required
def istek_sikayet_sakin(request):
    if request.user.role != "sakin":
        return HttpResponseForbidden("Erişim reddedildi.")

    if request.method == 'POST':
        form = IstekSikayetForm(request.POST)
        if form.is_valid():
            kayit = form.save(commit=False)
            kayit.user = request.user
            kayit.save()
            return redirect('istek_sikayet_sakin')  # refresh
    else:
        form = IstekSikayetForm()
    istekler = IstekSikayet.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'istek_sikayet_k.html', {'form': form, 'istekler': istekler})


@login_required
def istek_sikayet_personel(request):
    if request.user.role != "personel":
        return HttpResponseForbidden("Erişim reddedildi.")

    if request.method == 'POST':
        form = IstekSikayetForm(request.POST)
        if form.is_valid():
            kayit = form.save(commit=False)
            kayit.user = request.user
            kayit.save()
            return redirect('istek_sikayet_personel')
    else:
        form = IstekSikayetForm()

    istekler = IstekSikayet.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'istek_sikayet_p.html', {
        'form': form,
        'istekler': istekler
    })


@login_required
def admin_istek_sikayet_paneli(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    istekler = IstekSikayet.objects.filter(kategori='istek').order_by('-created_at')
    sikayetler = IstekSikayet.objects.filter(kategori='sikayet').order_by('-created_at')

    return render(request, 'istek_sikayet.html', {
        'istekler': istekler,
        'sikayetler': sikayetler,
    })