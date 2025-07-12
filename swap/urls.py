from django.urls import path
from . import views

urlpatterns = [
    path('', views.swap_list, name='swap_list'),
    path('delete/<int:pk>/', views.delete_swap, name='delete_swap'),
    path('request/<int:skill_id>/<int:receiver_id>/', views.initiate_swap, name='initiate_swap'),
    path('complete/<int:swap_id>/', views.complete_swap, name='complete_swap'),
]
