import requests


class pokeApiRequests():

    def get_pokemon_by_loc(location):
        pokemon = []
        x = requests.get('https://pokeapi.co/api/v2/pokedex/' + location).json()

        for i in x["pokemon_entries"]:
            pokemon.append(i["pokemon_species"]["name"])

        return pokemon

    def get_first_type_by_pokemon(pokemon):
        x = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon).json()

        type = x["types"][0]["type"]["name"]

        return type