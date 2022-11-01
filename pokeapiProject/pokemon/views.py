from django.shortcuts import render
from django.http import HttpResponse

from pokeApi.requests import pokeApiRequests, SearchPokemonColours


def index(request):
    pokemon_colour_list = []

    pokemon_list = pokeApiRequests.get_pokemon_by_loc("kanto")
    
    colours = SearchPokemonColours().get_colours()

    for i in colours:
        pokemon_colour_list.append(i[0])

    context = {"pokemon": pokemon_list, "type": pokemon_colour_list}

    return render(request, 'index.html', context)


def home(request):
    context = {"name":"user"}
    return render(request, 'test.html', context)


def about(request):
    return render(request, 'test-about.html')
