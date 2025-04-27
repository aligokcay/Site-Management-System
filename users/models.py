from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        YONETICI = "yonetici", "Yönetici"
        SAKİN = "sakin", "Sakin"
        PERSONEL = "personel", "Personel"
    
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.YONETICI,
    )


      # --- Daire Bilgileri ---
    blok = models.CharField(max_length=10,blank=True, null=True)  # Örn: A, B, C gibi blok isimleri
    kat = models.PositiveIntegerField(blank=True, null=True)     # Kat numarası, örnek: 1, 2, 3
    daire_no = models.CharField(max_length=3,blank=True, null=True)  # 3 haneli olacak, örnek: "006", "102", "210"

    uid = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )  
    # Otomatik üretilecek: blok + kat + daire_no birleşimi, Örn: "A306", "B201"

    # --- Kiracı Bilgileri ---
    kirada_mi = models.BooleanField(default=False)  # True ise kiracı var
    mevcut_sakin = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )  
    # Kiracı ismi: "Ahmet Yılmaz" gibi; yoksa "Kiracı Yok" gibi bir ifade

    kira_durumu = models.CharField(max_length=20, default="Ödenmedi")
    aidat_durumu = models.CharField(max_length=20, default="Ödenmedi")
    
    def save(self, *args, **kwargs):
            # Eğer kullanıcı EV SAKİNİ ise, blok, kat ve daire_no alanları zorunlu olacak
            if self.role == self.Roles.SAKİN:
                if not (self.blok and self.kat is not None and self.daire_no):
                    raise ValueError("Ev sakinleri için blok, kat ve daire_no alanları zorunludur.")

            # UID üretimi: Blok+Kat+DaireNo birleştirilecek
            if not self.uid and self.blok and self.kat is not None and self.daire_no:
                self.uid = f"{self.blok}{self.kat}{self.daire_no}"

            super().save(*args, **kwargs)

    def __str__(self):
        return self.uid or self.username # Admin panelinde kullanıcı adı yerine uid görünür
