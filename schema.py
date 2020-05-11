# The base of this project was this AirBNB Project:
# https://codeburst.io/how-to-build-a-graphql-wrapper-for-a-restful-api-in-python-b49767676630
# example request: {reviews(id:1238125) { comments } }

from graphene import ObjectType, String, Boolean, ID, List, Field, Int
from airbnb import Api
import json
import os
from collections import namedtuple
import requests
import xmltodict


# Due to quantitative access restrictions, a key is required to access BehindTheName.com's API. Enter yours here.
BEHIND_THE_NAME_API_KEY = "mi850283787"


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

### BehindTheName Classes ###
class NameUsage(ObjectType):
    usage_code = String()
    usage_full = String()
    usage_gender = String()

class Name(ObjectType):
    name = String()
    gender = String()
    usages = List(NameUsage)


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
    
    
    ### BehindTheName ###
    names = List(Name, name=String(required=True))
    
    @staticmethod
    def resolve_names(parent, info, name):
        
        URL = "https://www.behindthename.com/api/lookup.json"
        params = {"key": BEHIND_THE_NAME_API_KEY, "name": name}
        r = requests.get(URL, params=params)
        
        response_list = json2obj(json.dumps(r.json()))
        return response_list
        
    