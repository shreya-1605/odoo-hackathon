from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('add/', views.add_skill, name='add_skill'),
    path('<int:pk>/', views.skill_detail, name='skill_detail'),
    path('<int:pk>/edit/', views.edit_skill, name='edit_skill'),
    path('<int:pk>/delete/', views.delete_skill, name='delete_skill'),
]
