from django.shortcuts import render
from django.http import HttpResponse

from pokeApi.requests import pokeApiRequests, SearchPokemonColors


def index(request):

    pokemon_list = pokeApiRequests.get_pokemon_by_loc("kanto")
    
    colours = SearchPokemonColors().get_colors()

    count = 0
    for i in colours:
        pokemon_list[count]["color"] = i[0]
        count += 1

    context = {"details": pokemon_list}

    return render(request, 'index.html', context)


def home(request):
    context = {"name":"user"}
    return render(request, 'test.html', context)


def about(request):
    return render(request, 'test-about.html')
