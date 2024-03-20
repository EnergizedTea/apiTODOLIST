from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

tasks = []
BASE_URL = '/api/v1/'

@app.route('/')
def home():
    return 'Welcome to my To-Do List'

@app.route(BASE_URL + 'tasks', methods=['POST'])
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
        'category': request.json['category'],
        'created': this_time,
        'updated': this_time,
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route(BASE_URL + 'tasks', methods=['GET'])
def get_tasks():
      return jsonify({"tasks": tasks})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    print("TASK")
    if len(this_task) == 0:
        abort(404, error='ID not found!')
    return jsonify({'task': this_task[0]})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def update_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found!')

    if not request.json:
        abort(400, error='Missing body in request')

    updated_task = request.json
    if 'name' in updated_task:
        this_task[0]['name'] = updated_task['name']
    if 'category' in updated_task:
        this_task[0]['category'] = updated_task['category']

    this_task[0]['updated'] = datetime.now()

    return jsonify({'task': this_task[0]})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found!')
    tasks.remove(this_task[0])
    return jsonify({'result': True})

# THIS RIGHT HERE IS THE REASON OUR APP RUNS LET'S GOOOOOOOOOOOOOOOOOOOOOO
if __name__ == "__main__":
    # YOU BETTER MAKE SURE DEBUG IS SET TO FALSE WHEN YOU DEPLOY BOI
    app.run(debug=True)
