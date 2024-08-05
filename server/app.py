# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

@app.get('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.where(Earthquake.id == id).first()

    if earthquake:
        return earthquake.to_dict(), 200
    else:
        return {"message": f"Earthquake {id} not found."}, 404
    

@app.get("/earthquakes/magnitude/<float:magnitude>")
def get_min_earthquakes(magnitude):
    earthquakes = Earthquake.query.where(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    quakes = [earthquake_min.to_dict() for earthquake_min in earthquakes]
    return{"count":count, "quakes":quakes}




if __name__ == '__main__':
    app.run(port=5556, debug=True)
