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

    def type_effectiveness(type):
        double_damage_from = []
        normal_damage_from = []
        half_damage_from = []
        no_damage_from = []
        types = []

        x = requests.get('https://pokeapi.co/api/v2/type').json()["results"]
        for i in x:
            types.append(i["name"])
            if len(types) == 18:
                break

        type_details = requests.get('https://pokeapi.co/api/v2/type/' + type).json()["damage_relations"]

        if len(type_details["double_damage_from"]) != 0:
            for i in type_details["double_damage_from"]:
                double_damage_from.append(i["name"])
        if len(type_details["half_damage_from"]) != 0:
            for i in type_details["half_damage_from"]:
                half_damage_from.append(i["name"])
        if len(type_details["no_damage_from"]) != 0:
            for i in type_details["no_damage_from"]:
                no_damage_from.append(i["name"])

        for i in types:
            if i not in double_damage_from and i not in half_damage_from and i not in no_damage_from:
                normal_damage_from.append(i)

        type_eff = {
            "quad_damage_from": [],
            "double_damage_from": double_damage_from,
            "normal_damage_from": normal_damage_from,
            "half_damage_from": half_damage_from,
            "quarter_damage_from": [],
            "no_damage_from": no_damage_from,
        }

        return type_eff

    def validate_type_effectiveness(type_eff):
        new_type_eff = {
            "quad_damage_from": [],
            "double_damage_from": [],
            "normal_damage_from": [],
            "half_damage_from": [],
            "quarter_damage_from": [],
            "no_damage_from": [],
        }

        first_type = list(type_eff.values())[0]
        second_type = list(type_eff.values())[1]
        
        for i in first_type["double_damage_from"]:
            if i in second_type["double_damage_from"]:
                # Type 1 = 2x
                # Type 2 = 2x
                #--------------
                # Overall = 4x
                new_type_eff["quad_damage_from"].append(i)
            elif i in second_type["half_damage_from"]:
                # Type 1 = 2x
                # Type 2 = 1/2x
                #--------------
                # Overall = 1x
                new_type_eff["normal_damage_from"].append(i)
            elif i in second_type["no_damage_from"]:
                # Type 1 = 2x
                # Type 2 = 0x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)
            else:
                # Type 1 = 2x
                # Type 2 = 1x
                #--------------
                # Overall = 2x
                new_type_eff["double_damage_from"].append(i)
        
        for i in first_type["normal_damage_from"]:
            if i in second_type["double_damage_from"]:
                # Type 1 = 1x
                # Type 2 = 2x
                #--------------
                # Overall = 2x
                new_type_eff["double_damage_from"].append(i)
            elif i in second_type["half_damage_from"]:
                # Type 1 = 1x
                # Type 2 = 1/2x
                #--------------
                # Overall = 1/2x
                new_type_eff["half_damage_from"].append(i)
            elif i in second_type["no_damage_from"]:
                # Type 1 = 1x
                # Type 2 = 0x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)
            else:
                # Type 1 = 1x
                # Type 2 = 1x
                #--------------
                # Overall = 1x
                new_type_eff["normal_damage_from"].append(i)
        for i in first_type["half_damage_from"]:
            if i in second_type["double_damage_from"]:
                # Type 1 = 1/2x
                # Type 2 = 2x
                #--------------
                # Overall = 1x
                new_type_eff["normal_damage_from"].append(i)
            elif i in second_type["half_damage_from"]:
                # Type 1 = 1/2x
                # Type 2 = 1/2x
                #--------------
                # Overall = 1/4x
                new_type_eff["quarter_damage_from"].append(i)
            elif i in second_type["no_damage_from"]:
                # Type 1 = 1/2x
                # Type 2 = 0x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)
            else:
                # Type 1 = 1/2x
                # Type 2 = 1x
                #--------------
                # Overall = 1/2x
                new_type_eff["half_damage_from"].append(i)
        for i in first_type["no_damage_from"]:
            if i in second_type["double_damage_from"]:
                # Type 1 = 0x
                # Type 2 = 2x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)
            elif i in second_type["half_damage_from"]:
                # Type 1 = 0x
                # Type 2 = 1/2x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)
            elif i in second_type["no_damage_from"]:
                # Type 1 = 0x
                # Type 2 = 0x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)
            else:
                # Type 1 = 0x
                # Type 2 = 1x
                #--------------
                # Overall = 0x
                new_type_eff["no_damage_from"].append(i)

        return new_type_eff

    def get_pokemon_details(pokemon):
        type_eff = {}

        details = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon).json()

        type = [details["types"][0]["type"]["name"]]
        if len(details["types"]) > 1:
            type.append(details["types"][1]["type"]["name"])

        if len(type) == 1:
            type_eff = pokeApiRequests.type_effectiveness(type[0])

        if len(type) > 1:
            for i in type:
                type_eff[i] = pokeApiRequests.type_effectiveness(i)
            type_eff = pokeApiRequests.validate_type_effectiveness(type_eff)

        stats = {
            "hp": details["stats"][0]["base_stat"],
            "attack": details["stats"][1]["base_stat"],
            "defense": details["stats"][2]["base_stat"],
            "sp_atk": details["stats"][3]["base_stat"],
            "sp_def": details["stats"][4]["base_stat"],
            "speed": details["stats"][5]["base_stat"],
        }

        height = details["height"] / 10
        weight = details["weight"] / 10

        details = {
            "pokemon": pokemon,
            "type_eff": type_eff,
            "stats": stats,
            "height": height,
            "weight": weight,
        }

        return details


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
            result = row

        connection_obj.close()        

        return result