from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('skill-assessment/<str:product_type>/', views.skill_assessment_view, name='skill_assessment'),
    path('notification-preferences/', views.notification_preferences_view, name='notification_preferences'),
]