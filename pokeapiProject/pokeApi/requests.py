import requests
import sqlite3


class pokeApiRequests():

    def get_pokemon_by_loc(location):
        """ 
        Returns the pokemon names from the location name.
        
        Keyword arguments:
        location -- string -- the name of the location (Kanto, Johto etc.)
        """
        pokemon = []
        x = requests.get('https://pokeapi.co/api/v2/pokedex/' + location).json()

        for i in x["pokemon_entries"]:
            pokemon.append({"name":i["pokemon_species"]["name"]})

        return pokemon

    def get_first_type_by_pokemon(pokemon):
        """
        Returns the first typing for a given Pokemon.

        *Currently not used*

        Keyword arguments:
        pokemon -- string -- The name of the pokemon
        """
        x = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon).json()

        type = x["types"][0]["type"]["name"]

        return type

    def type_effectiveness(type):
        """
        Returns a dicitonary with the damage information for a given type.  

        Gets the type details from the PokeAPI.
        Loops through each damage info section and, if it contains entries, adds them to a list.
        If a move is not mentioned in the JSON object sent back from the API then it is added to the normal_damage list.
        All the lists are added to a dicitonary.
        Quad and Quarter damage entries are added for compatibility reasons even though one type Pokemon will never have a Quad weakness.

        Keyword arguments:
        type -- string -- The type name (Fairy, Normal etc.)
        """

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
        """
        Given two types it returns a new dictionary with type effectiveness.

        If the first typing and the second typing take double damage from the same type, then the Pokemon is quad weak to that type...
        These new type damage stats are added to a new dicitonary for the Pokemon.
        This new dictionary is returned to replace the previous dicitonary going forward.

        Keyword arguments:
        type_eff -- dict -- Dictionary with both types' weaknesses
        """
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
        """
        The main method to get details for the Pokemon wiki page. Returns a dictionary with all necessary details.

        Gets the details from PokeAPI.
        Adds the type to a list and then checks if the Pokemon has another type, if they do it is also added to the list.
        If the Pokemon only has one type, send it to the type_effectiveness function to get back the dicitonary of it's weaknesses.
        If the Pokemon has 2 types, do the above for BOTH types, then send all these weaknesses to the validate_type_effectiveness 
        function to get back their combined weaknesses.
        Get the base stats for the Pokemon and add them to a dictionary.
        Get the height of the Pokemon.
        Get the weight of the Pokemon.
        Add all the dicitonaries to a new dictionary called details and return this to the parent function.

        Keyword arguments:
        pokemon -- string -- The name of the Pokemon
        """

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
            "color": type[0],
            "type_eff": type_eff,
            "stats": stats,
            "height": height,
            "weight": weight,
        }

        return details


class SearchPokemonColors:
    def search_all():
        db = sqlite3.connect("Pokemon.db")
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM POKEMON_FIRST_TYPE''')
        items = cursor.fetchall()
        db.close()

        return items


    def get_colors():
        db = sqlite3.connect("Pokemon.db")
        cursor = db.cursor()
        cursor.execute('''SELECT colour FROM POKEMON_FIRST_TYPE''')
        results = cursor.fetchall()
        db.close()

        return results 


    def get_colour_by_pokemon(pokemon):
        db = sqlite3.connect("Pokemon.db")
        cursor = db.cursor()
        cursor.execute('''SELECT colour FROM POKEMON_FIRST_TYPE WHERE pokemon = ? ''' , (pokemon,))
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
        data=cursor_obj.execute('''SELECT * FROM CAUGHT_POKEMON''')

        connection_obj.commit()
        
        connection_obj.close()

    def update_caught_pokemon(name,pokemon):
        connection_obj = sqlite3.connect("Pokemon.db")
        cursor_obj = connection_obj.cursor()

        cursor_obj.execute('''UPDATE CAUGHT_POKEMON SET Pokemon = ? WHERE Name = ?''', (str(pokemon), name ))

        data=cursor_obj.execute('''SELECT * FROM CAUGHT_POKEMON''')

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