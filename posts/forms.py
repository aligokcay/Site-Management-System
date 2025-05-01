from django import forms
from .models import Duyuru, IstekSikayet

class DuyuruForm(forms.ModelForm):
    class Meta:
        model = Duyuru
        fields = ['title', 'content']

class IstekSikayetForm(forms.ModelForm):
    class Meta:
        model = IstekSikayet
        fields = ['kategori', 'konu', 'aciklama']
