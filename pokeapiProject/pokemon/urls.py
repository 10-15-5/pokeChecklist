from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graphs/', views.graphs, name='graphs'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('wiki', views.pokemon_details, name='wiki'),
]