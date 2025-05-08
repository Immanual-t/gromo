from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('set-goals/', views.set_goals_view, name='set_goals'),
    path('add-sale/', views.add_sale_view, name='add_sale'),
    path('refresh-card/<str:card_id>/', views.refresh_card_view, name='refresh_card'),
]