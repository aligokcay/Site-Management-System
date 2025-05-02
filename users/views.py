import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages

def home(request):
    return render(request, "index-dark.html")

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"Authenticate başarılı: {user.username}")
            if user.role == role:  # Kullanıcının rolü doğru mu kontrol et
                login(request, user)  # Django kullanıcıyı sisteme dahil eder

                # Role göre doğru panele yönlendir
                if user.role == CustomUser.Roles.YONETICI:
                    return redirect('/panel-yonetici.html')
                elif user.role == CustomUser.Roles.SAKİN:
                    return redirect('/panel-sakin.html')
                elif user.role == CustomUser.Roles.PERSONEL:
                    return redirect('/panel_personel_static')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Rol eşleşmedi!")
                # Rol eşleşmiyorsa hata
                return redirect('home')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı!")
            # Kullanıcı adı veya şifre yanlışsa
            return redirect('home')
    else:
        return redirect('home')



@login_required
def panel_yonetici_static(request):
    return render(request, 'panel-yonetici.html')

@login_required
def panel_sakin_static(request):
    return render(request, 'panel_sakin_static')

@login_required
def panel_personel_static(request):
    return render(request, 'panel-personel.html')


def custom_logout(request):
    logout(request)
    return redirect('home') 


@csrf_exempt
def daire_guncelle(request):
    if request.method == 'POST':
        print("POST geldi.")
        data = json.loads(request.body)
        print("Gelen data:", data)

        blok = data.get('blok')
        kat = data.get('kat')
        daire_no = data.get('daire_no')
        mevcut_sakin = data.get('mevcut_sakin')
        kirada_mi = data.get('kirada_mi', False)

        print(f"Aranıyor -> Blok: {blok}, Kat: {kat}, Daire No: {daire_no}")

        try:
            daire = CustomUser.objects.get(blok=blok, kat=kat, daire_no=daire_no)
            print("Daire bulundu:", daire)
            daire.mevcut_sakin = mevcut_sakin
            daire.kirada_mi = kirada_mi
            daire.save()
            print("Daire güncellendi.")
            return JsonResponse({'message': 'Başarıyla güncellendi!'})
        except CustomUser.DoesNotExist:
            print("Daire bulunamadı!")
            return JsonResponse({'error': 'Daire bulunamadı.'}, status=404)

    print("Geçersiz istek!")
    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)


def daire_bilgileri(request):
    daireler = CustomUser.objects.filter(role=CustomUser.Roles.SAKİN)
    return render(request, 'daire-info.html', {'daireler': daireler})

def kira_takip(request):
    daireler = CustomUser.objects.filter(role=CustomUser.Roles.SAKİN)
    return render(request, 'aidat-takip.html', {'daireler': daireler})

