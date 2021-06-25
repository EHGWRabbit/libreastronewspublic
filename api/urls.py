from django.urls import path 
from .views import bbs #список новостей
from .views import BbDetailView#вывод отдельных сведений о выбранной новости
from .views import comments #вывод и добавление комментариев



urlpatterns = [
    path('bbs/<int:pk>/comments/', comments),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', bbs),
]