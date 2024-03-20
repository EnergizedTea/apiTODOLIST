from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    created = db.Column(datetime(timezone=True), server_default=func.now())
    updated = db.Column(datetime(timezone=True), onupdate=func.now())
    status = db.Column(db.Boolean, default=False)

    # Representación
    def _repr_(self):
        if self.updated is None:
            return f'<Task {self.name} under {self.category} with status {self.updated} created {self.created}>'
        else:
            return f'<Task {self.name} under {self.category} with status {self.updated} created {self.created} and updated {self.updated}>'
            

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
