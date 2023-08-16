#!/usr/bin/python3
"""
    This module starts a Flask Web App
    that interacts with our AirBnB engine
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    """
        Displays the list of all states in alphabetical order
        in an HTML page
    """
    states = storage.all(State)
    stateList = [state for state in states.values()]
    srtStates = sorted(stateList, key=lambda s: s.name)
    return render_template("9-states.html", states=srtStates)


@app.route("/states/<id>", strict_slashes=False)
def states_list_id(id):
    """
        Displays the list of all states in alphabetical order
        in an HTML page
    """
    states = storage.all(State)
    stateList = [state for state in states.values()]
    srtStates = sorted(stateList, key=lambda s: s.name)
    existingIDs = list(map(lambda state: state.id, srtStates))
    return render_template("9-states.html", states=srtStates,
                           id=id, existingIDs=existingIDs)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the DB session """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
