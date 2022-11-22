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


class DatabaseActions:

    def create_table():
        connection_obj = sqlite3.connect("Pokemon.db")
        cursor_obj = connection_obj.cursor()
        
        cursor_obj.execute("DROP TABLE IF EXISTS CAUGHT_POKEMON")
        
        # Creating table
        table = """ CREATE TABLE CAUGHT_POKEMON (
                    Name CHAR(25) UNIQUE,
                    Pokemon
                ); """
        
        cursor_obj.execute(table)
        
        print("Table is Ready")
        
        connection_obj.close()

    def insert_caught_pokemon(name,pokemon):
        connection_obj = sqlite3.connect("Pokemon.db")
        cursor_obj = connection_obj.cursor()

        cursor_obj.execute('''INSERT INTO CAUGHT_POKEMON VALUES (?, ?)''', (name, str(pokemon)))

        print("Data Inserted in the table: ")
        data=cursor_obj.execute('''SELECT * FROM CAUGHT_POKEMON''')
        # for row in data:
        #     print(row)

        connection_obj.commit()
        
        connection_obj.close()

    def update_caught_pokemon(name,pokemon):
        connection_obj = sqlite3.connect("Pokemon.db")
        cursor_obj = connection_obj.cursor()

        cursor_obj.execute('''UPDATE CAUGHT_POKEMON SET Pokemon = ? WHERE Name = ?''', (str(pokemon), name ))

        data=cursor_obj.execute('''SELECT * FROM CAUGHT_POKEMON''')
        # for row in data:
        #     print(row)

        connection_obj.commit()
        
        connection_obj.close()

    
    def search_caught_pokemon(name):
        connection_obj = sqlite3.connect("Pokemon.db")
        cursor_obj = connection_obj.cursor()

        result = cursor_obj.execute("SELECT Pokemon FROM CAUGHT_POKEMON WHERE Name=?", (name,))

        for row in result:
            print(row)

        connection_obj.close()        

        return result