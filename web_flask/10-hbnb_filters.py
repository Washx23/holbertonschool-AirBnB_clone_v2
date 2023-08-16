#!/usr/bin/python3
"""
    This module starts a Flask Web App
    that interacts with our AirBnB engine
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def states_list():
    """
        Displays tthe AirBnB console with dynamic HTML
        interacting with our engine.
    """
    stateList = [state for state in storage.all(State).values()]
    amenityList = [amenity for amenity in storage.all(Amenity).values()]

    return render_template("10-hbnb_filters.html",
                           states=stateList, amenities=amenityList)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the DB session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
