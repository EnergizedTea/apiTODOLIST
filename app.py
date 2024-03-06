from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

tasks = []
BASE_URL = '/api/v1/'


@app.route('/')
def home():
    return 'Welcome to my To-Do List'


@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(400, error = 'Missing body in request')
    if 'name' not in request.json:
        return jsonify({"ERROR":"Missing name"}), 400
    if 'category' not in request.json:
        return jsonify({"ERROR":"Missing category"}), 400
    this_time = datetime.now()
    task = {
        'id': len(tasks) + 1,
        'name': request.json['name'],
        'category': False,
        'created': this_time,
        'updated': this_time,
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# THIS RIGHT HERE IS THE REASON OUR APP RUNS LET'S GOOOOOOOOOOOOOOOOOOOOOO
if __name__ == "__main__":
    # YOU BETTER MAKE SURE DEBUG IS SET TO FALSE WHEN YOU DEPLOY BOI
    app.run(debug=True)
