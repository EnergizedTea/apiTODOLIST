from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import credentials

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = credentials.url

db = SQLAlchemy(app)
BASE_URL = '/api/v1/'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, default=False)


    def show(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'status': self.status
        }
    

@app.route('/')
def home():
    return 'Welcome to my To-Do List'

@app.route(BASE_URL + 'create', methods=['POST'])
def createTask():
    if not request.json:
        abort(400, error = 'Missing body in request')
    if 'name' not in request.json:
        abort(400, error = 'Missing name in request')
    if 'category' not in request.json:
        abort(400, error = 'Missing category in request')
    
    task = Task(name=(request.json['name']), category=(request.json['category']), status=False)
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'Created task succesfully!': task.show()}), 201

@app.route(BASE_URL + 'create/<int:id>', methods=['POST'])
def createTaskWithId(id):
    if not request.json:
        abort(400, error = 'Missing body in request')
    if 'name' not in request.json:
        abort(400, error = 'Missing name in request')
    if 'category' not in request.json:
        abort(400, error = 'Missing category in request')
    if Task.query.get(id) is None:
        task = Task(id=id,name=(request.json['name']), category=(request.json['category']), status=False)
        db.session.add(task)
        db.session.commit()
        
        return jsonify({'Created task succesfully!': task.show()}), 201
    else:
        return jsonify({'Id already in existace'}), 409

@app.route(BASE_URL + 'change/<int:id>', methods=['PATCH'])
def updateTask(id):
    task = Task.query.get(id)
    if task is None:
        abort(404, error="Task not found!")
        
    if 'name' and 'category' not in request.json:
        abort(400, error = 'No body, nothing to change')
        
    if 'name' in request.json:
        task.name = request.json['name']
    if 'category'in request.json:
        task.category = request.json['category']
        
    db.session.commit()
    return jsonify('Task has been changed has been succesfully changed'), 200
    
@app.route(BASE_URL + 'tasks', methods=['GET'])
def getTasks():
    allTasks = Task.query.all()
    return jsonify({'These are all your tasks': [task.show() for task in allTasks]}), 200

@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def getTask(id):
    task = Task.query.get(id)
    if task is None:
        abort(404, error="Task not found!")
    return jsonify({'This is the task you asked for': task.show()}), 200

@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def deleteTask(id):
    task = Task.query.get(id)
    if task is None:
        abort(404, error="Task not found!")
    db.session.delete(task)
    db.session.commit()
    
    return jsonify('Task has been deleted'), 200


    
# THIS RIGHT HERE IS THE REASON OUR APP RUNS LET'S GOOOOOOOOOOOOOOOOOOOOOO
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created...")

    # YOU BETTER MAKE SURE DEBUG IS SET TO FALSE WHEN YOU DEPLOY BOI
    app.run(debug=True)
