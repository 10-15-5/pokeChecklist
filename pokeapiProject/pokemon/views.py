from django.shortcuts import render
from django.http import HttpResponse

from pokeApi.requests import pokeApiRequests


def index(request):
    pokemon_type_list = []

    pokemon_list = pokeApiRequests.get_pokemon_by_loc("kanto")

    # for i in pokemon_list:
    #     type = pokeApiRequests.get_first_type_by_pokemon(i)
    #     pokemon_type_list.append(type)
    # print(pokemon_type_list)

    context = {"pokemon": pokemon_list, "type":""}

    return render(request, 'index.html', context)


def home(request):
    context = {"name":"user"}
    return render(request, 'test.html', context)


def about(request):
    return render(request, 'test-about.html')
