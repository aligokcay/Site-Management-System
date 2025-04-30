from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Duyuru
from .forms import DuyuruForm

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