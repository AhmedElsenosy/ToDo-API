from django.urls import path
from . import views

urlpatterns = [
    path('create-task/', views.create_task, name='create_task'),
    path('get-tasks/', views.get_all_tasks, name='get_all_tasks'),
    path('get-task/<str:pk>', views.get_task, name='get_task'),
]
