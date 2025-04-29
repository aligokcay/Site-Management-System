
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


