#!/usr/bin/python3
"""
    This module starts a Flask Web App
    that interacts with our AirBnB engine
"""


from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Display a list of all State objects present in DBStorage"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Display a list of City objects linked to the State"""
    state = storage.get(State, id)
    if state:
        return render_template('9-states_cities.html', state=state)
    return render_template('9-not_found.html')


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
