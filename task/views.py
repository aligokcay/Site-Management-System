from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser, Calisan
from task.models import Task

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

            from datetime import date

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

    return render(request, 'personel-takip.html', {
        'personeller': personeller,
        'gorevler': gorevler,
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