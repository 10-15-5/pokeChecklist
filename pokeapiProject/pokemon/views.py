from django.shortcuts import render
from django.http import HttpResponse
import requests


def index(request):

    x = requests.get('https://pokeapi.co/api/v2/pokedex/kanto').json()

    context = {"name": x["pokemon_entries"]}

    return render(request, 'test.html', context)


def home(request):
    context = {"name":"user"}
    return render(request, 'test.html', context)


def about(request):
    return render(request, 'test-about.html')
