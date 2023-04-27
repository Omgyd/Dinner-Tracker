from flask import Flask, render_template, request, redirect, url_for
from mongo import get_current_poll, update_vote

app = Flask(__name__)


@app.route("/")
def index():
    current_poll = get_current_poll("Today")
    return render_template('index.html', poll=current_poll)


@app.route("/vote", methods=["POST"])
def vote():
    if request.method == "POST":
        dish_name = request.form.get("dish")
        update_vote(dish_name, "Today")
    return redirect(url_for("index"))