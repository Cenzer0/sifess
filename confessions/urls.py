from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/grid/', views.dashboard_grid, name='dashboard_grid'),
    path('confession/<uuid:pk>/pin/', views.pin_confession, name='pin_confession'),
    path('confession/<uuid:pk>/delete/', views.delete_confession, name='delete_confession'),
    path('confession/<uuid:pk>/like/', views.like_confession, name='like_confession'),
    path('<slug:slug>/', views.public_profile, name='public_profile'),
]
