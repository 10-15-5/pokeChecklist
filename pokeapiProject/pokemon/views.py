from django.shortcuts import render
from django.http import HttpResponse

from pokeApi.requests import pokeApiRequests, SearchPokemonColors, DatabaseActions
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')


def index(request):

    pokemon_list = pokeApiRequests.get_pokemon_by_loc("kanto")
    
    colours = SearchPokemonColors().get_colors()

    response = DatabaseActions.search_caught_pokemon(request.user.username)

    count = 0
    if type(response) is tuple:
        for i in colours:
            pokemon_list[count]["color"] = i[0]

            if pokemon_list[count]["name"] in response[0]:
                pokemon_list[count]["caught"] = "true"
            else:
                pokemon_list[count]["caught"] = "false"

            count += 1
    else:
        for i in colours:
            pokemon_list[count]["color"] = i[0]
            pokemon_list[count]["caught"] = "false"
            count += 1

    context = {"details": pokemon_list}

    return render(request, 'index.html', context)


def thanks(request):

    pokemon_caught = request.POST.getlist('pokemon')

    response = DatabaseActions.search_caught_pokemon(request.user.username)

    if type(response) is tuple:
        DatabaseActions.update_caught_pokemon(request.user.username, pokemon_caught)
    else:
        DatabaseActions.insert_caught_pokemon(request.user.username, pokemon_caught)

    context = {"pokemon":pokemon_caught}
    return render(request, 'thanks.html', context)


def about(request):
    return render(request, 'test-about.html')
