from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_face_view, name='login_face'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_attendance/', views.mark_attendance_view, name='mark_attendance'),
    path('logout/', views.custom_logout, name='logout'),
    
]


