from django.urls import path
from . import views

urlpatterns = [
    path('top_apps/', views.top_apps, name='top_apps'),
    path('api/update-top-apps/', views.update_top_apps, name='update_top_apps'),
    path('api/get-top-apps/', views.get_apps, name='get_top_apps'),
]