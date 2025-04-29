from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title','assigned_to__username',)

