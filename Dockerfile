FROM python:3.9-slim-buster
WORKDIR /dinner-tracker
COPY ./requirements.txt /dinner-tracker
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=dinner_tracker.py
CMD gunicorn -w 4 -b  0.0.0.0:8000 --access-logfile - "dinner_tracker:create_app()"