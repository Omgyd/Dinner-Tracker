import os
import uuid
import random
from pymongo import MongoClient
from dotenv import load_dotenv
from sheets import get_dish_list

load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))

db = client["test-database"]

dishes = db.dishes
polls = db.polls



def add_dish():
    for x in get_dish_list():
        record = {"_id": uuid.uuid4().hex, 'dish': x[0], 'ingredients': x[1], 'time': x[2]}
        if dishes.find_one({'dish': x[0]}):
            print("Dish already in database")
        else:
            dishes.insert_one(record)

def get_dishes():
    dishes_dict = {}
    for x in dishes.find():
        dishes_dict[x['dish']] = {'ingredients': x['ingredients'], 'time': x['time']}
    return dishes_dict
        
def get_dish(dish_name):
    dish = dishes.find_one({'dish': dish_name})
    return dish

def create_poll_options():
    dish_list = get_dishes()
    random_list = []
    while len(random_list) < 3:
        choice = random.choice(list(dish_list))
        if choice not in random_list:
            random_list.append(choice)
        else:
            continue
    return random_list










