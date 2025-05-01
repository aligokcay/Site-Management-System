from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta, datetime, time
from .models import Tesis, Randevu

@login_required
def randevu_panel(request):
    tesisler = Tesis.objects.all()
    bugun = date.today()
    tarihler = [date.today() + timedelta(days=i) for i in range(7)]
    max_tarih = bugun + timedelta(days=7)
    uygun_saatler = []
    tarih_str = ""
    secilen_tesis = request.GET.get("tesis")
    tarih_raw = request.GET.get("tarih")

    # Tarih parse et
    if tarih_raw:
        try:
            tarih = datetime.strptime(tarih_raw, "%Y-%m-%d").date()
            tarih_str = tarih.strftime("%Y-%m-%d")
        except ValueError:
            tarih = None
    else:
        tarih = None

    # Uygun saatleri bul
    if secilen_tesis and tarih:
        try:
            tesis = get_object_or_404(Tesis, ad=secilen_tesis)
            saatler = [time(h, 0) for h in range(9, 23)]
            for saat in saatler:
                varsa = Randevu.objects.filter(tesis=tesis, tarih=tarih, saat=saat).exists()
                if not varsa:
                    uygun_saatler.append(saat)
        except:
            pass

    # POST işleminde randevu kaydet
    if request.method == "POST":
        tesis_adi = request.POST.get("tesis")
        tarih_str = request.POST.get("tarih")
        saat_str = request.POST.get("saat")

        if tesis_adi and tarih_str and saat_str:
            try:
                tesis = get_object_or_404(Tesis, ad=tesis_adi)
                tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()
                saat = datetime.strptime(saat_str, "%H:%M").time()

                # Önceden alınmış mı kontrol et
                dolu = Randevu.objects.filter(tesis=tesis, tarih=tarih, saat=saat).exists()
                if not dolu:
                    Randevu.objects.create(kullanici=request.user, tesis=tesis, tarih=tarih, saat=saat)
                    return redirect("randevu_panel")
            except:
                pass

    return render(request, "randevu.html", {
        "bugun": bugun,
        "max_tarih": max_tarih,
        "tarih_str": tarih_str,
        "tarihler": tarihler,
        "tesisler": tesisler,
        "uygun_saatler": uygun_saatler,
    })