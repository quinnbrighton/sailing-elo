from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sailing.db'  # Use 'mysql://username:password@localhost/db_name' for MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''
# Define database models
class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(50))
    #venue = db.Column(db.String(100))
    #wind_speed = db.Column(db.String(50))
    #wind_direction = db.Column(db.String(50))
'''
class Skipper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(50))
    year = db.Column(db.Integer)
    adjusted_estimate = db.Column(db.Float)
    std_error = db.Column(db.Float)
    z_value = db.Column(db.Float)
    p_value = db.Column(db.Float)
'''
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    wind_speed = db.Column(db.String(50))
    wind_direction = db.Column(db.String(50))
'''
    #python -c "from app import db; db.create_all()"

@app.route('/')
def home():
    #races = Race.query.all()
    skippers = Skipper.query.order_by(Skipper.id).limit(3).all()
    print(skippers)
    #venues = Venue.query.all()
    #conditions = Weather.query.all()
    #return render_template('index.html', races=races, skippers=skippers, venues=venues, conditions=conditions)
    return render_template('home.html', skippers=skippers)

    