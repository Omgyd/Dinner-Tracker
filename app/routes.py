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
)
from app.forms import LoginForm, RegisterForm
from app import app


if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    sched = BackgroundScheduler()
    sched.add_job(create_poll, "cron", hour=0)
    sched.start()


if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    sched = BackgroundScheduler()
    sched.add_job(create_poll, "cron", hour=0, minute=0, timezone="US/Eastern")
    sched.start()


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("email"):
        return redirect(url_for("login"))
    today = today_at_midnight()
    current_poll = get_current_poll(today)
    # print(current_poll)
    return render_template("index.html", poll=current_poll, date=today)


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


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))
