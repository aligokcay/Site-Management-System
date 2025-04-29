from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('create/', views.task_create, name='task_create'),
]
