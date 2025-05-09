from django.contrib import admin
from .models import Task, Aidat, GorevUyari, AidatUyari
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title','assigned_to__username',)
    


@admin.register(Aidat)
class AidatAdmin(admin.ModelAdmin):
    list_display = ('user', 'donem', 'tutar', 'odeme_durumu', 'dekont','son_odeme_tarihi' )
    fields = ('user','donem','tutar','odeme_durumu','dekont','son_odeme_tarihi')
    list_filter = ('odeme_durumu', 'son_odeme_tarihi')
    search_fields = ('user__username', 'donem', 'tutar')
    list_editable = ('odeme_durumu', 'son_odeme_tarihi')
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.odeme_durumu:
            return ['user', 'donem', 'tutar', 'dekont', 'son_odeme_tarihi']
        return super().get_readonly_fields(request, obj)


@admin.register(GorevUyari)
class GorevUyariAdmin(admin.ModelAdmin):
    list_display = ('user', 'gorev', 'mesaj', 'olusturma_tarihi')
    list_filter = ('olusturma_tarihi',)
    search_fields = ('user__username', 'gorev__title', 'mesaj')

@admin.register(AidatUyari)
class AidatUyariAdmin(admin.ModelAdmin):
    list_display = ('user', 'aidat', 'mesaj', 'olusturma_tarihi')
    list_filter = ('olusturma_tarihi',)
    search_fields = ('user__username', 'aidat__donem', 'mesaj')