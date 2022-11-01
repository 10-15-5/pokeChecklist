import requests
import sqlite3


class pokeApiRequests():

    def get_pokemon_by_loc(location):
        pokemon = []
        x = requests.get('https://pokeapi.co/api/v2/pokedex/' + location).json()

        for i in x["pokemon_entries"]:
            pokemon.append({"name":i["pokemon_species"]["name"]})

        return pokemon

    def get_first_type_by_pokemon(pokemon):
        x = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon).json()

        type = x["types"][0]["type"]["name"]

        return type


class SearchPokemonColors:
    def __init__(self, pokemon=None, colour=None):
        self.pokemon = pokemon
        self.colour = colour


    def search_all(self):
        db = sqlite3.connect("Pokemon.db")
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM POKEMON_COLOURS''')
        items = cursor.fetchall()
        db.close()

        return items


    def get_colors(self):
        db = sqlite3.connect("Pokemon.db")
        cursor = db.cursor()
        cursor.execute('''SELECT colour FROM POKEMON_COLOURS''')
        results = cursor.fetchall()
        db.close()

        return results 


    def get_colour_by_pokemon(self):
        db = sqlite3.connect("Pokemon.db")
        cursor = db.cursor()
        cursor.execute('''SELECT colour FROM POKEMON_COLOURS WHERE pokemon = ? ''' , (self.pokemon,))
        results = cursor.fetchone()
        db.close()

        return results