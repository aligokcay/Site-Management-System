from django.db import models
from django.conf import settings

class Duyuru(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class IstekSikayet(models.Model):
    class Tip(models.TextChoices):
        ISTEK = 'istek', 'İstek'
        SIKAYET = 'sikayet', 'Şikayet'

    tur = models.CharField(max_length=10, choices=Tip.choices)
    content = models.TextField()
    olusturan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tur.capitalize()} - {self.olusturan.username}"
