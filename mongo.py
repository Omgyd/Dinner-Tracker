import os
import uuid
import random
import datetime as dt
from pymongo import MongoClient
from dotenv import load_dotenv
from sheets import get_dish_list

load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))

db = client["test-database"]

dishes = db.dishes
poll = db.poll



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


def create_poll():
    poll_options = create_poll_options()
    day_poll = {
            "_id": uuid.uuid4().hex,
            poll_options[0]: {"Votes": 0},
            poll_options[1]: {"Votes": 0}, 
            poll_options[2]: {"Votes": 0},
            "date": "Today"
            }
    poll.insert_one(day_poll)


def get_current_poll(date):
    todays_poll = poll.find_one({"date": date}, {'_id': 0, 'date': 0})
    return todays_poll



def update_vote(dish, date):
    poll_to_update = get_current_poll(date)
    vote_count = poll_to_update[dish]["Votes"]
    new_vote = {"$set": {dish: {"Votes": vote_count + 1}}}
    poll.update_one(poll_to_update, new_vote)

def set_votes_zero():
    for item in get_current_poll("Today"):
        new_vote = {"$set": {item: {"Votes": 0}}}
        poll.update_one(get_current_poll("Today"), new_vote)  







