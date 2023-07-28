from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit/', views.edit_image, name='edit_image'),
    path('result/', views.result, name='result'),  # Add this line
]
