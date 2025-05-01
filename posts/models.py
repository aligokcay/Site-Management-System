from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Duyuru(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class IstekSikayet(models.Model):
    KATEGORI_CHOICES = [
        
        ('istek', 'İstek'),
        ('sikayet', 'Şikayet'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    konu = models.CharField(max_length=255)
    aciklama = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kategori.capitalize()} - {self.konu} ({self.user.username})"

    @property
    def kullanici_gorunumu(self):
        if self.user.role == "personel":
            return self.user.get_full_name()
        elif self.user.role == "sakin":
            return self.user.mevcut_sakin
        return self.user.username