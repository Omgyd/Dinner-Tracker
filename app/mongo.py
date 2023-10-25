import os
import uuid
import random
import datetime as dt
from flask import redirect, render_template, flash, url_for, session
from dotenv import load_dotenv

from .models import User, Grocery
from passlib.hash import pbkdf2_sha256
from dataclasses import asdict

# from app.sheets import get_dish_list
# from app import db
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))

db = client["test-database"]


dishes = db.dishes
poll = db.poll
users = db.users
votes = db.votes
grocery= db.grocery


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
        dishes_dict[x["dish"]] = {"ingredients": x["ingredients"], "time": x["time"]}
    return dishes_dict


def get_dish(dish_name):
    dish = dishes.find_one({"dish": dish_name})
    return dish

def get_dish_ingredients(dish_name):
    dish = get_dish(dish_name)
    ingredients = [x.strip() for x in dish['ingredients'].split(',')]
    return ingredients


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
        "total_votes": 0,
    }
    _id = poll.insert_one(day_poll)
    votes.insert_one({"poll_id": _id.inserted_id, "date": today, "voted": []})


def get_current_poll(date):
    todays_poll = poll.find_one({"date": date}, {"_id": 0, "date": 0})
    return todays_poll


def update_vote(dish, date, user):
    poll_to_update = poll.find_one({"date": date})
    vote_count = poll_to_update[dish]["Votes"]
    voted_list = votes.find_one({"poll_id": poll_to_update["_id"]})
    if user in voted_list["voted"]:
        flash("You have already voted")
        return redirect("index.html")
    new_vote = {"$set": {dish: {"Votes": vote_count + 1}}, "$inc": {"total_votes": 1}}
    new_voter = {"$push": {"voted": user}}
    poll.update_one(poll_to_update, new_vote)
    votes.update_one(voted_list, new_voter)


def get_current_winner(date):
    winning_votes = 0
    winner = "There is no current winner!"
    if get_current_poll(date) == None:
        return "There is no current winner!"
    for item, votes in get_current_poll(date).items():
        if item != "total_votes":
            if votes["Votes"] > winning_votes:
                winning_votes = votes["Votes"]
                winner = item
    return winner


def set_votes_zero():
    today = today_at_midnight()
    current_poll = poll.find_one({"date": today})
    voters = votes.find_one({"poll_id": current_poll["_id"]})
    zero_voters = {"$set": {"voted": None}}
    for item in get_current_poll(today):
        new_vote = {"$set": {item: {"Votes": 0}}}
        new_total = {"$set": {"total_votes": 0}}
        poll.update_one(get_current_poll(today), new_vote)
        poll.update_one(get_current_poll(today), new_total)
    votes.update_one(voters, zero_voters)


def register_user(form):
    today = today_at_midnight
    email_found = users.find_one({"email": form.email.data})
    if email_found:
        flash("Email is already registered.")
        return render_template("register.html")
    else:
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            group_id = uuid.uuid4().hex
        )
        grocery_list = Grocery(
            _id=user.group_id,
            items = []
        )
        users.insert_one(asdict(user))
        grocery.insert_one(asdict(grocery_list))

        flash("User registered successfully", "success")


def login_user(form):
    user_data = users.find_one({"email": form.email.data})
    if not user_data:
        flash("Login credentials not correct", category="danger")
        return redirect(url_for("login"))
    user = User(**user_data)
    if user and pbkdf2_sha256.verify(form.password.data, user.password):
        session["user_id"] = user._id
        session["email"] = user.email
        session['name'] = user.first_name
        session['group_id'] = user.group_id
        return redirect(url_for("index"))

def get_grocery_list(user):
    return user

# This function will pass in a users first name and use that to search for their group_id.
# Change this later to also accept the target user to update the id and remove the names.
def update_id(user):
    primary_user = users.find_one({"first_name": user})
    group_id = primary_user['group_id']
    filter = {"email": "Amaralowry@gmail.com"}
    new_data = {"$set": {"first_name": "Amara", "last_name": "Lowry", "group_id": group_id }}
    users.update_one(filter, new_data)




