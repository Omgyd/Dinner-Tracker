from flask import Flask, render_template
import random
from mongo import get_dishes, create_poll_options

app = Flask(__name__)


@app.route("/")
def index():
    poll_options = create_poll_options()
    return render_template('index.html', poll_options=poll_options)