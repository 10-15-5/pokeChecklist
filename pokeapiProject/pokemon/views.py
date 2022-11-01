from django.shortcuts import render
from django.http import HttpResponse

from pokeApi.requests import pokeApiRequests, SearchPokemonColors
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')


def index(request):

    pokemon_list = pokeApiRequests.get_pokemon_by_loc("kanto")
    
    colours = SearchPokemonColors().get_colors()

    count = 0
    for i in colours:
        pokemon_list[count]["color"] = i[0]
        count += 1

    context = {"details": pokemon_list}

    # print(request.user.username)

    return render(request, 'index.html', context)


def thanks(request):

    pokemon_caught = request.POST.getlist('pokemon')

    context = {"pokemon":pokemon_caught}
    return render(request, 'thanks.html', context)


def about(request):
    return render(request, 'test-about.html')
