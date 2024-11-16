from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

df = pd.read_csv("data/skippers.csv")
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
    __tablename__ = 'skippers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(50))
    year = db.Column(db.Integer)
    adjusted_estimate = db.Column(db.Float)
    std_error = db.Column(db.Float)
    z_value = db.Column(db.Float)
    p_value = db.Column(db.Float)
    rating = db.Column(db.Integer)
    school_name = db.Column(db.String(100))
    image_token = db.Column(db.String(100))
    school_token = db.Column(db.String(100))
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

def get_top_skaters_by_school(df, school_name):
    if school_name:
        filtered_df = df[df['School Name'].str.contains(school_name, case=False, na=False)]  # Filters skippers by school
    else:
        filtered_df = df  # If no school is specified, return the whole DataFrame
    return filtered_df

@app.route('/get_top_skippers', methods=['GET'])
def get_top_skippers():
    school_name = request.args.get('school_name', '')  # Get the school name from the query string
    top_skaters = get_top_skaters_by_school(df, school_name)
    
    # Prepare the data in JSON format
    result = top_skaters.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
    return jsonify(result)



@app.route('/')
def home():
    #races = Race.query.all()
    skippers = Skipper.query.limit(50).all()
    #venues = Venue.query.all()
    #conditions = Weather.query.all()
    #return render_template('index.html', races=races, skippers=skippers, venues=venues, conditions=conditions)
    return render_template('home.html', skippers=skippers)

    