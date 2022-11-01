from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thank-you/', views.thanks, name='thanks'),
    path('about/', views.about, name='about'),
]