"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from users.views import custom_login, home,  panel_yonetici_static, custom_logout, daire_bilgileri, daire_guncelle, kira_takip, panel_sakin_static, panel_personel_static
from task.views import personel_takip_view, calisan_gorevleri
from posts.views import duyuru_listesi, duyuru_ekle, duyuru_k, duyuru_p
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('', home, name='home'), 
    path('panel-yonetici.html', panel_yonetici_static, name='panel_yonetici_static'),
    path('panel-sakin.html', panel_sakin_static, name='panel_sakin_static'),
    path('panel-personel.html', panel_personel_static, name='panel_personel_static'),
    path('daireler/', daire_bilgileri, name='daire_bilgileri'),
    path('daire-guncelle/', daire_guncelle, name='daire_guncelle'),
    path('kira-takip/', kira_takip, name='kira_takip'),
    path('personel-takip/', personel_takip_view, name='personel_takip'),
    path('gorevlerim/', calisan_gorevleri, name='calisan_gorevleri'),
    path('duyurular/', duyuru_listesi, name='duyuru_listesi'),
    path('duyuru-ekle/', duyuru_ekle, name='duyuru_ekle'),
    path('duyuru-k/', duyuru_k, name='duyuru_k'), 
    path('duyuru-p/', duyuru_p, name='duyuru_p'),
    

]

urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'assets'))
