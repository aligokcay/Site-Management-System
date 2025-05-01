from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tesis(models.Model):
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad

class Randevu(models.Model):
    kullanici = models.ForeignKey(User , on_delete=models.CASCADE)
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    tarih = models.DateField()
    saat = models.TimeField()
    olusturulma = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tesis', 'tarih', 'saat')  # Aynı saatte bir kişi olabilir

    def __str__(self):
        return f'{self.tesis} - {self.tarih} {self.saat}'
