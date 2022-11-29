import re
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from pokeApi.requests import pokeApiRequests, SearchPokemonColors, DatabaseActions

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .forms import SignUpForm


@login_required(login_url='/signup/')


def index(request):

    pokemon_list = pokeApiRequests.get_pokemon_by_loc("kanto")
    
    colours = SearchPokemonColors.get_colors()

    response = DatabaseActions.search_caught_pokemon(request.user.username)

    count = 0
    if type(response) is tuple:

        response_list = re.sub(r"[\[\]'\s]", "", response[0])
        response_list = response_list.split(",")

        for i in colours:
            pokemon_list[count]["color"] = i[0]

            if pokemon_list[count]["name"] in response_list:
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

    return render(request, 'home.html', context)


def graphs(request):
    pokemon_types = {
        "normal": 0,
        "fire": 0,
        "water": 0,
        "electric": 0,
        "grass": 0,
        "ice": 0,
        "fighting": 0,
        "poison": 0,
        "ground": 0,
        "flying": 0,
        "psychic": 0,
        "bug": 0,
        "rock": 0,
        "ghost": 0,
        "dragon": 0,
        "dark": 0,
        "steel": 0,
        "fairy": 0
    }
    
    pokemon_caught = request.POST.getlist('pokemon')
    len_pokemon_caught = len(request.POST.getlist('pokemon'))
    pokemon_missing = 151 - len_pokemon_caught
    percent_caught = round((len_pokemon_caught / 151)*100)

    response = DatabaseActions.search_caught_pokemon(request.user.username)

    if type(response) is tuple:
        DatabaseActions.update_caught_pokemon(request.user.username, pokemon_caught)
    else:
        DatabaseActions.insert_caught_pokemon(request.user.username, pokemon_caught)

    for i in pokemon_caught:
        first_type = SearchPokemonColors.get_colour_by_pokemon(i)[0]
        
        pokemon_types[first_type] += 1

    context = {
        "pokemon_caught": len_pokemon_caught, 
        "pokemon_missing": pokemon_missing,
        "percent_caught": percent_caught,
        "types_caught": pokemon_types,
    }
    return render(request, 'graphs.html', context)


def about(request):
    return render(request, 'test-about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def pokemon_details(request):
    details = pokeApiRequests.get_pokemon_details(request.GET.get("pokemon"))

    return render(request, 'wiki.html', details)