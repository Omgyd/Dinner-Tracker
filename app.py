import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for
from mongo import get_current_poll, update_vote, today_at_midnight, create_poll, register_user


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
  sched = BackgroundScheduler()
  sched.add_job(create_poll,'cron', hour=0)
  sched.start()

@app.route("/")
def index():
    today = today_at_midnight()
    current_poll = get_current_poll(today)
    return render_template('index.html', poll=current_poll, date=today)


@app.route("/vote", methods=["POST"])
def vote():
    today = today_at_midnight()
    if request.method == "POST":
        dish_name = request.form.get("dish")
        update_vote(dish_name, today)
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        register_user(email, username, password1, password2)
    return render_template("register.html")