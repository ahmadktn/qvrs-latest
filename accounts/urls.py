from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/student/', views.student_register_view, name='register_student'),
    path('dashboard/', views.dashboard_dispatcher_view, name='dashboard'),
]
