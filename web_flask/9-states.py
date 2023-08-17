#!/usr/bin/python3
"""
    This module starts a Flask Web App
    that interacts with our AirBnB engine
"""


from flask import Flask, render_template
from models import storage, State, City


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def display_states():
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def display_state_cities(id):
    state = storage.get(State, id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('state.html', state=state, cities=cities)
    else:
        return render_template('not_found.html')


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
