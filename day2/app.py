from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect, Document, StringField
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB
connect('person_db', host='localhost', port=27017)

class Person(Document):
    name = StringField(required=True, max_length=100)
    gender = StringField(required=True, choices=['Male', 'Female', 'Other'])
    location = StringField(required=True, max_length=200)

# Create a Person
@app.route('/person', methods=['POST'])
def add_person():
    data = request.json
    person = Person(
        name=data['name'],
        gender=data['gender'],
        location=data['location']
    )
    person.save()
    return jsonify({'message': 'Person added successfully', 'id': str(person.id)}), 201

# Get all Persons
@app.route('/person', methods=['GET'])
def get_all_persons():
    persons = Person.objects()
    person_list = [{**person.to_mongo().to_dict(), '_id': str(person.id)} for person in persons]
    return jsonify(person_list), 200

# Get a Person by ID
@app.route('/person/<string:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.objects(id=ObjectId(person_id)).first()
    if person:
        person_data = person.to_mongo().to_dict()
        person_data['_id'] = str(person.id)
        return jsonify(person_data), 200
    return jsonify({'error': 'Person not found'}), 404

# Update a Person
@app.route('/person/<string:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    person = Person.objects(id=ObjectId(person_id)).first()
    if person:
        person.update(**data)
        return jsonify({'message': 'Person updated successfully'}), 200
    return jsonify({'error': 'Person not found'}), 404

# Delete a Person
@app.route('/person/<string:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.objects(id=ObjectId(person_id)).first()
    if person:
        person.delete()
        return jsonify({'message': 'Person deleted successfully'}), 200
    return jsonify({'error': 'Person not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
