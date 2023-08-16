#!/usr/bin/python3
"""
    This module starts a Flask Web App
    that interacts with our AirBnB engine
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """
        Displays the list of all states and their respective cities
        in alphabetical order in an HTML page
    """
    states = storage.all(State)
    stateList = [state for state in states.values()]
    srtStates = sorted(stateList, key=lambda s: s.name)
    return render_template("8-cities_by_states.html", states=srtStates)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the DB session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
