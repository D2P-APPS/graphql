# The base of this project was this AirBNB Project:
# https://codeburst.io/how-to-build-a-graphql-wrapper-for-a-restful-api-in-python-b49767676630
# example request: {reviews(id:1238125) { comments } }

from graphene import ObjectType, String, Boolean, ID, List, Field, Int, Float
from airbnb import Api
import json
import os
from collections import namedtuple
import requests
import xmltodict


#############
# FUNCTIONS #
#############

def _json_object_hook(d):
    return namedtuple('X', d.keys(), rename=True)(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

###########
# CLASSES #
###########

### PokéAPI Classes ###

# This is a generic object for storing any object type with two elements: "name" and "url"
# Based on the construction of this API, this covers several different types of objects,
# including game version, item, ability, and several others.
class Object(ObjectType):
    name = String()
    url = String()

class AbilityListObject(ObjectType):
    ability = Field(Object)
    is_hidden = Boolean
    slot = Int()

class GameIndex(ObjectType):
    game_index = Int()
    version = Field(Object)

class ItemVersionDetail(ObjectType):
    rarity = Int()
    version = Field(Object)

class Item(ObjectType):
    item = Field(Object)
    version_details = List(ItemVersionDetail)

class ItemListObject(ObjectType):
    item = Field(Object)
    version_details = List(ItemVersionDetail)

class MoveVersionDetail(ObjectType):
    level_learned_at = Int()
    move_learn_method = Field(Object)
    version_group = Field(Object)

class MoveObject(ObjectType):
    move = Object()
    version_group_details = List(MoveVersionDetail)

class Sprites(ObjectType):
    back_default = String()
    back_female = String()
    back_shiny = String()
    back_shint_female = String()
    front_default = String()
    front_female = String()
    front_shiny = String()
    front_shint_female = String()

class Stat(ObjectType):
    base_stat = Int()
    effort = Int()
    stat = Field(Object)
    
class Type(ObjectType):
    slot = Int()
    type = Field(Object)

class Pokemon(ObjectType):
    abilities = List(AbilityListObject)
    base_experience = Int()
    forms = List(Object)
    game_indices = List(GameIndex)
    height = Int()
    held_items = List(ItemListObject)
    id = ID()
    is_default = Boolean()
    location_area_encounters = String()
    moves = List(MoveObject)
    name = String()
    order = Int()
    species = Field(Object)
    sprites = Sprites()
    stats = List(Stat)
    types = List(Type)
    weight = Int()


### AirBNB Classes ###
class User(ObjectType):
    first_name = String()
    has_profile_pic = Boolean()
    id = ID()
    picture_url = String()
    smart_name = String()
    thumbnail_url = String()

class Listing(ObjectType):
    id = ID()
    name = String()

class Review(ObjectType):
    author = Field(User)
    author_id = ID()
    can_be_edited = Boolean()
    comments = String()
    created_at = String()
    id = Int()
    language = String()
    listing = Field(Listing)
    listing_id = ID()
    recipient = Field(User)
    recipient_id = ID()
    response = String()
    role = String()
    user_flag = Boolean()
    

#####################
# QUERIES/MUTATIONS #
##################### 
            
class Query(ObjectType):

    ### AirBNB ###
    reviews = List(Review, id=Int(required=True))

    @staticmethod
    def resolve_reviews(parent, info, id):
    
        api = Api(os.environ.get("AIRBNB_LOGIN"), 
                  os.environ.get("AIRBNB_PASSWORD"))
        response = api.get_reviews(id)["reviews"]
        response_list = json2obj(json.dumps(response))
        return response_list
    
    
    ### PokéAPI ###
    pokemon_by_name = Field(Pokemon, name=String(required=True))
    
    @staticmethod
    def resolve_pokemon_by_name(parent, info, name):
        
        URL = f"https://www.pokeapi.co/api/v2/pokemon/{name.lower()}"
        
        r = requests.get(URL)
        
        response_obj = json2obj(json.dumps(r.json()))
        
        return response_obj
        
    