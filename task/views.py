from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from users.models import CustomUser, Calisan
from task.models import Task, Aidat, GorevUyari, AidatUyari
from task.forms import AidatForm, DekontForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from datetime  import date, timedelta
from django.utils.timezone import now
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse





User = get_user_model()

def is_admin(user):
    return user.is_superuser 


def personel_takip_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'personel_ekle':
            ad_soyad = request.POST.get('ad_soyad')
            job_title = request.POST.get('job_title')

            isimler = ad_soyad.split()
            first_name = isimler[0]
            last_name = ' '.join(isimler[1:]) if len(isimler) > 1 else ''

            # 1. önce CustomUser oluştur
            user = CustomUser.objects.create_user(
                username=(first_name + last_name).lower(),
                email=first_name.lower() + last_name.lower() + "@example.com",
                first_name=first_name,
                last_name=last_name,
                password="123456",  # istersen şimdilik default şifre
                role=CustomUser.Roles.PERSONEL
            )

            # 2. sonra Calisan kaydı yap
            Calisan.objects.create(
                user=user,
                job_title=job_title
            )

        elif form_type == 'gorev_ekle':
            calisan_id = request.POST.get('calisan_id')
            title = request.POST.get('title')
            end_date = request.POST.get('end_date')
            status = request.POST.get('status')

            calisan = Calisan.objects.get(id=calisan_id)

            Task.objects.create(
                assigned_to=calisan,
                title=title,
                start_date=date.today(),  # otomatik bugünün tarihi
                end_date=end_date,
                status=status
            )

        return redirect('personel_takip')  # POST işlemi bitince sayfayı yenile

    # GET işlemi
    personeller = Calisan.objects.all()
    gorevler = Task.objects.all()

    today = date.today()

    return render(request, 'personel-takip.html', {
        'personeller': personeller,
        'gorevler': gorevler,
        'today': today,
    })

@login_required
def calisan_gorevleri(request):
    try:
        calisan = Calisan.objects.get(user=request.user)
        gorevler = Task.objects.filter(assigned_to=calisan)
    except Calisan.DoesNotExist:
        gorevler = []

    return render(request, 'gorev_p.html', {
        'gorevler': gorevler,
    })






def aidat_toplu_ekle(request):
    if request.method == "POST":
        form = AidatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Aidat ve dekont kaydedildi.")
            return redirect('aidat_listesi')
        donem = request.POST.get("donem")  # Örn: "2025-05"
        tutar = request.POST.get("tutar")

        sakinler = User.objects.filter(role='sakin')

        sayac = 0
        for user in sakinler:
            mevcut_sakin = user.mevcut_sakin or user.get_full_name()
            aidat, created = Aidat.objects.get_or_create(
                user=user,
            defaults={
                'tutar': tutar,
                'mevcut_sakin': mevcut_sakin,
                'odeme_durumu': 'Bekleniyor',
            }
        )
        if created:
            user.aidat_durumu = 'Ödenmedi'
            user.save()
            donem=donem,
            defaults={
                    'tutar': tutar,
                    'mevcut_sakin': mevcut_sakin,
                    'odeme_durumu': 'Bekleniyor',
                }
            sayac += 1

        messages.success(request, f"{sayac} adet aidat kaydı başarıyla eklendi.")
        return redirect("aidat_takip.html")

    return render(request, "")

@login_required
def dekont_yukle(request, pk):
    aidat = get_object_or_404(Aidat, pk=pk, user=request.user)
    if request.method == 'POST':
        # the file input is named "dekont"
        dekont_file = request.FILES.get('dekont')
        if dekont_file and dekont_file.content_type == 'application/pdf':
            aidat.dekont = dekont_file
            aidat.save()
            messages.success(request, "Dekontunuz başarıyla yüklendi; yönetici onayını bekleyin.")
            return redirect('sakin_aidat_takip')
        else:
            messages.error(request, "Lütfen geçerli bir PDF dosyası yükleyin.")
    # if GET or invalid POST, just go back
    return redirect('sakin_aidat_takip')



def admin_aidat_list(request):
    # Yeni aidat yaratma
    if request.method == 'POST' and 'create_aidat' in request.POST:
        form = AidatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yeni aidat oluşturuldu.")
            return redirect('admin_aidat_list')
        else:
            messages.error(request, "Lütfen formu doğru doldurun.")
    else:
        form = AidatForm()

    # Sakinin yüklediği dekontları onaylama
    if request.method == 'POST' and 'approve_pk' in request.POST:
        aidat = get_object_or_404(Aidat, pk=request.POST['approve_pk'])
        aidat.odeme_durumu = True
        from django.utils.timezone import now
        aidat.odeme_tarihi = now().date()
        aidat.save()
        messages.success(request, f"{aidat.donem} dönemi onaylandı.")
        return redirect('admin_aidat_list')
    today= timezone.now().date()
    unpaid = Aidat.objects.filter(odeme_durumu=False).order_by('-donem')
    return render(request, 'aidat-takip.html', {
        'form': form,
        'aidatlar': unpaid,
        'today': today,
    })

def admin_aidat_approve(request, pk):
    aidat = get_object_or_404(Aidat, pk=pk)
    aidat.odeme_durumu = True
    aidat.odeme_tarihi = timezone.now().date()
    aidat.save()
    messages.success(request, "Aidat ödendi olarak işaretlendi.")
    return redirect('admin_aidat_list')

def admin_create_aidat(request):
    if request.method == "POST":
        tutar = request.POST.get("tutar")
        donem = request.POST.get("donem")
        if not (tutar and donem):
            messages.error(request, "Lütfen tutar ve dönemi doldurun.")
            return redirect('admin_aidat_list')

        created = 0
        users = User.objects.filter(role='sakin')
        for u in users:
            obj, was_created = Aidat.objects.get_or_create(
                user=u,
                donem=donem,
                defaults={
                    'tutar': tutar,
                    'son_odeme_tarihi': date.fromisoformat(donem + "-01"),
                }
            )
            if was_created:
                created += 1

        messages.success(request, f"{created} yeni aidat kaydı oluşturuldu (dönem: {donem}).")
    return redirect('admin_aidat_list')


def aidat_yonetici(request):


    # --- BÜYÜK AİDAT OLUŞTURMA ---
    if request.method == "POST" and 'do_bulk_create' in request.POST:
        tutar_raw = request.POST.get('bulk_tutar')
        try:
            tutar = float(tutar_raw)
            donem = now().strftime("%Y-%m")
            today = now().date()
            # Bir sonraki ayın 1. günü
            if today.month == 12:
                next_month = today.replace(year=today.year+1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month+1, day=1)
            son_odeme_tarihi = next_month - timedelta(days=1)
            sakins = User.objects.filter(role='sakin')
            say = 0
            for u in sakins:
                if not Aidat.objects.filter(user=u, donem=donem).exists():
                    Aidat.objects.create(
                        user=u,
                        donem=donem,
                        tutar=tutar,
                        son_odeme_tarihi=son_odeme_tarihi
                    )
                    say += 1
            messages.success(request, f"{say} adet aidat ({donem}) oluşturuldu.")
        except ValueError:
            messages.error(request, "Lütfen geçerli bir tutar girin.")
        # POST sonrası GET’e yönlendir
        return redirect('aidat_takip')  # URL adınız neyse

    aidatlar = Aidat.objects.filter(odeme_durumu=False).order_by('-donem')
    unpaid = aidatlar.exists()
    today = now().date()
    return render(request, 'aidat-takip.html', {
        'aidatlar': aidatlar,
        'unpaid': unpaid,
        'today': today,
    })

@login_required
def aidat_kullanici_view(request):
    aidatlar = Aidat.objects.filter(user=request.user).order_by('-donem')
    return render(request, 'aidat-kullanıcı.html', {
        'aidatlar': aidatlar,
    })

def get_today_context():
    return {'today': date.today()}

@login_required
@csrf_exempt
def gorev_uyar(request):
    context = get_today_context()
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        task = get_object_or_404(Task, id=task_id)

        GorevUyari.objects.create(
            user=task.assigned_to.user,
            gorev=task,
            mesaj="Görevin süresi geçti, lütfen kontrol ediniz."
        )
        messages.success(request, "Uyarı başarıyla gönderildi.")
    return redirect("personel_takip")



@require_POST
def gorev_tamamla(request, pk):
    gorev = get_object_or_404(Task, pk=pk)
    gorev.status = "tamamlandi"
    gorev.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))



# @login_required
# def panel_personel_view(request):
#     uyarilar = GorevUyari.objects.filter(user=request.user).order_by('-olusturma_tarihi')
#     if not uyarilar.exists():
#         print("Henüz bir uyarınız yok.")
#     else:
#         print(f"{uyarilar.count()} adet uyarınız var.")
#         return render(request, 'panel-personel.html', {'uyarilar': uyarilar})
@login_required
def panel_personel_view(request):
    uyarilar = GorevUyari.objects.filter(user=request.user).order_by('-olusturma_tarihi')
    return render(request, 'panel-personel.html', {'uyarilar': uyarilar})
    



@login_required
@csrf_exempt
def aidat_uyar(request):
    if request.method == "POST":
        aidat_id = request.POST.get("aidat_id")
        aidat = get_object_or_404(Aidat, id=aidat_id)

        if not aidat.odeme_durumu and aidat.son_odeme_tarihi < timezone.now().date():
            AidatUyari.objects.create(
                user=aidat.user,
                aidat=aidat,
                mesaj="Aidat ödemeniz gecikti, lütfen en kısa sürede ödeme yapınız."
            )
            messages.success(request, "Aidat uyarısı başarıyla gönderildi.")
        else:
            messages.warning(request, "Uyarı gerekli değil. Aidat zaten ödendi ya da son ödeme tarihi geçmedi.")

    return redirect("aidat_takip")  # buradaki view adına göre düzenleyebilirsin


@login_required
def panel_sakin_view(request):
    print("Panel sakin view çalıştı.")
    aidat_uyarilar = AidatUyari.objects.filter(user=request.user).order_by('-olusturma_tarihi')

    return render(request, 'panel-sakin.html', {
        'uyarilar': aidat_uyarilar,
    })

