# app.py

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

def create_app(testing=False):
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/reminders_db'
    app.config['TESTING'] = testing
    
    mongo = PyMongo(app)
    
    if testing:
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_reminders_db'

    db = mongo.db

    @app.route('/reminders', methods=['POST'])
    def create_reminder():
        data = request.json
        if not all(k in data for k in ('userId', 'type', 'dateTime', 'description')):
            return jsonify({'message': 'Todos os campos são obrigatórios.'}), 400

        reminder = {
            'userId': ObjectId(data['userId']),
            'type': data['type'],
            'dateTime': datetime.fromisoformat(data['dateTime']),
            'description': data['description'],
            'createdAt': datetime.utcnow()
        }

        result = db.reminders.insert_one(reminder)
        reminder['_id'] = str(result.inserted_id)

        return jsonify({'message': 'Lembrete criado com sucesso!', 'reminder': reminder}), 201

    @app.route('/reminders/<userId>', methods=['GET'])
    def get_reminders(userId):
        reminders = db.reminders.find({'userId': ObjectId(userId)}).sort('dateTime', 1)
        reminders_list = [{'type': r['type'], 'dateTime': r['dateTime'].isoformat(), 'description': r['description']} for r in reminders]

        return jsonify(reminders_list), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
