from django.contrib import admin
from .models import Duyuru, IstekSikayet

@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


@admin.register(IstekSikayet)
class IstekSikayetAdmin(admin.ModelAdmin):
    list_display = ('kategori', 'konu', 'user__username','kullanici_gorunumu', 'created_at')
    list_filter = ('kategori', 'created_at')
    search_fields = ('konu', 'aciklama', 'user__username', 'user__mevcut_sakin')
    readonly_fields = ('user', 'created_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')



