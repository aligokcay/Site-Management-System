# aidat/forms.py
from django import forms
from .models import Aidat

class AidatForm(forms.ModelForm):
    class Meta:
        model = Aidat
        fields = ['user', 'donem', 'tutar', 'son_odeme_tarihi']
        

class DekontForm(forms.ModelForm):
    class Meta:
        model = Aidat
        fields = ['dekont']
        