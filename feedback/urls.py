from django.urls import path
from . import views

urlpatterns = [
    path('leave/<int:skill_id>/', views.leave_feedback, name='leave_feedback'),
]
