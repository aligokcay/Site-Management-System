
from django.db import models
from django.conf import settings
from users.models import Calisan

class Task(models.Model):
    assigned_to = models.ForeignKey(Calisan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('beklemede', 'Beklemede'),
        ('tamamlandi', 'Tamamlandı'),
        ('gecikmis', 'Gecikmiş'),
    ], default='beklemede')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.assigned_to.user.get_full_name()} - {self.title}"

class Aidat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="aidatlar")
    donem = models.CharField(max_length=20)  # Örn: "2025-05"
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    odeme_durumu = models.BooleanField(default=False)
    odeme_tarihi = models.DateField(blank=True, null=True)
    dekont = models.FileField(
        upload_to='dekontlar/%Y/%m/',
        null=True,
        blank=True,
        help_text="PDF formatında dekont yükleyin."
    )
    son_odeme_tarihi = models.DateField()

    

    class Meta:
        unique_together = ('user', 'donem')

    def __str__(self):
        return f"{self.user} - {self.donem} - {'Ödendi' if self.odeme_durumu else 'Ödenmedi'}"
    def save(self, *args, **kwargs):
        # Eğer dekont dosyası varsa, odendi bayrağını True yap
        if self.dekont and not  self.odeme_durumu:
            self.odendi = True
        super().save(*args, **kwargs)