#!/usr/bin/python3
"""
    This module starts a Flask Web App
    that interacts with our AirBnB engine
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
        Displays the list of all states in alphabetical order
        in an HTML page
    """
    states = storage.all(State)
    stateList = [(state.id, state.name) for state in states.values()]
    srtStates = sorted(stateList, key=lambda s: s[1])
    return render_template("7-states_list.html", states=srtStates)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the DB session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
