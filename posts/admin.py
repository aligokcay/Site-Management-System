from django.contrib import admin
from .models import Duyuru, IstekSikayet

@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(IstekSikayet)
class IstekSikayetAdmin(admin.ModelAdmin):
    list_display = ('tur', 'olusturan', 'created_at')
    list_filter = ('tur',)
    search_fields = ('content',)
