import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for, session
from app.mongo import (
    get_current_poll,
    update_vote,
    today_at_midnight,
    create_poll,
    register_user,
    login_user,
    get_current_winner,
    get_dish_ingredients,
    get_grocery_list,
    add_item
)
from app.forms import LoginForm, RegisterForm, GroceryForm
from app import app


if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    sched = BackgroundScheduler()
    sched.add_job(create_poll, "cron", hour=0, timezone="US/Eastern")
    sched.start()


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("email"):
        return redirect(url_for("landing"))
    today = today_at_midnight()
    current_poll = get_current_poll(today)
    current_winner = get_current_winner(today)
    # print(current_poll)
    return render_template(
        "index.html", poll=current_poll, date=today, current_winner=current_winner
    )


@app.route("/vote", methods=["GET", "POST"])
def vote():
    today = today_at_midnight()
    user = session.get("email")
    if request.method == "POST":
        dish_name = request.form.get("dish")
        update_vote(dish_name, today, user)
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("email"):
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        register_user(form)
        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if login_user(form):
            return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route("/user", methods=["GET", "POST"])
def user_home():
    user = session.get("name")
    return render_template("user_home.html", user=user)

@app.route("/grocery-list", methods=["GET", "POST"])
def grocery_list():
    form = GroceryForm()
    user = session.get("group_id")
    grocery_list = get_grocery_list(user)
    if form.validate_on_submit():
        add_item(user, form)
        return redirect(url_for("grocery_list"))
    return render_template("grocery_list.html", grocery_list=grocery_list, form=form)

@app.route("/update_list", methods=["POST"])
def update_list():
    checked_items = request.form.getlist("checkbox")
    print("Checked Items:", checked_items)
    return "Completed"


# Test for funciton in in Jinja template, replace with function to get ingredients for each dish.
@app.context_processor
def utility_processor():
    def dish_func(dish):
        return get_dish_ingredients(dish)
    return dict(dish_func=dish_func)

@app.route("/home")
def landing():
    return render_template('landing.html')


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))
