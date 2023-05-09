import os
import uuid
import random
import datetime as dt
from flask import redirect, render_template, flash, url_for
from dotenv import load_dotenv
# from app.sheets import get_dish_list
# from app import db
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))

db = client['test-database']



dishes = db.dishes
poll = db.poll
users = db.users
votes = db.votes

def today_at_midnight():
    today = dt.datetime.today()
    return dt.datetime(today.year, today.month, today.day)

# Function to import dish info from google spreadsheet
# def add_dish():
#     for x in get_dish_list():
#         record = {"_id": uuid.uuid4().hex, 'dish': x[0], 'ingredients': x[1], 'time': x[2]}
#         if dishes.find_one({'dish': x[0]}):
#             print("Dish already in database")
#         else:
#             dishes.insert_one(record)

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
    today = today_at_midnight()
    day_poll = {
            "_id": uuid.uuid4().hex,
            poll_options[0]: {"Votes": 0},
            poll_options[1]: {"Votes": 0}, 
            poll_options[2]: {"Votes": 0},
            "date": today,
            }
    _id = poll.insert_one(day_poll)
    votes.insert_one({'poll_id': _id.inserted_id, 'date': today, 'voted': []})



def get_current_poll(date):
    todays_poll = poll.find_one({"date": date}, {'_id': 0, 'date': 0})
    return todays_poll



def update_vote(dish, date, user):
    poll_to_update = poll.find_one({'date': date})
    vote_count = poll_to_update[dish]["Votes"]
    voted_list = votes.find_one({'poll_id': poll_to_update['_id']})
    if user in voted_list['voted']:
        flash("You have already voted")
        return redirect("index.html")
    new_vote = {"$set": {dish: {"Votes": vote_count + 1}}}
    new_voter = {'$push': {'voted': user}}
    poll.update_one(poll_to_update, new_vote)
    votes.update_one(voted_list, new_voter)

def set_votes_zero():
    today = today_at_midnight()
    current_poll = poll.find_one({'date': today})
    voters = votes.find_one({'poll_id': current_poll['_id']})
    zero_voters = {'$set': {'voted': None}}
    for item in get_current_poll(today):
        new_vote = {"$set": {item: {"Votes": 0}}}
        poll.update_one(get_current_poll(today), new_vote) 
    votes.update_one(voters, zero_voters)

    
def register_user(email, username, password1, password2):
    today = today_at_midnight
    user_found = users.find_one({'user': username})
    email_found = users.find_one({'email': email})
    if user_found:
        flash("User is already registered.")
        return render_template("register.html")
    if email_found:
        flash("Email is already registered.")
        return render_template("register.html")
    if password1 != password2:
        flash("Passwords should match, please try again.")
        return render_template('register.html')
    else:
        password = password2
        user_info = {'email': email, 'user': username, 'password': password}
        users.insert_one(user_info)
        return redirect('index.html', date=today)
    
def login_user(email, password):
    user = users.find_one({'email': email})
    user_password = user['password']
    if password == user_password:
        return True
    else:
        print("Incorrect Username or Password")