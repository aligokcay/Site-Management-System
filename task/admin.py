from django.contrib import admin
from .models import Task, Aidat

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title','assigned_to__username',)
    


@admin.register(Aidat)
class AidatAdmin(admin.ModelAdmin):
    list_display = ('user', 'donem', 'tutar', 'odeme_durumu')
    readonly_fields = ('user','donem','tutar')
    fields = ('user','donem','tutar','odeme_durumu','dekont')
    # böylece admin, mevcut aidatı seçip sadece dekont yükleyebilir
