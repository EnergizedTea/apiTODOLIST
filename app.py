from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'status': self.status
        }
    

@app.route('/')
def home():
    return 'Welcome to my To-Do List'

@app.route('/create', methods=['POST'])
def create_task():
    if not request.json:
        abort(400, error = 'Missing body in request')
    if 'name' not in request.json:
        return jsonify({"ERROR":"Missing name"}), 400
    if 'category' not in request.json:
        return jsonify({"ERROR":"Missing category"}), 400
    
    task = Task(name=(request.json['name']), category=(request.json['category']), status=False)
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201



# THIS RIGHT HERE IS THE REASON OUR APP RUNS LET'S GOOOOOOOOOOOOOOOOOOOOOO
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created...")

    # YOU BETTER MAKE SURE DEBUG IS SET TO FALSE WHEN YOU DEPLOY BOI
    app.run(debug=True)
