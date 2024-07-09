#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# Disable SQLAlchemy track modifications to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set JSON response formatting to not compact
app.json.compact = False

# Initialize Flask-Migrate
migrate = Migrate(app, db)
# Initialize SQLAlchemy
db.init_app(app)

# Define a route for the root URL
@app.route('/')
def index():
    # Return a simple message for the root URL
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Define a route to get earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_by_id(id):
    # Query the database for the earthquake with the specified ID
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    # If earthquake is found, return its attributes as JSON response
    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        # If earthquake is not found, return 404 status with an error message
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    return make_response(body, status)

# Define a route to get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    # Query the database for earthquakes with magnitude greater than or equal to the specified value
    big_quakes = []
    for quake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        big_quakes.append(quake.to_dict())
    body = {
        'count': len(big_quakes),
        'quakes': big_quakes
    }
    status = 200
    return make_response(body, status)

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5555, debug=True)