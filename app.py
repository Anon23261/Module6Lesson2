from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
ma = Marshmallow(app)

# Database configuration using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'yourusername')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'yourpassword')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'fitness_center')

# Initialize MySQL connection
try:
    db = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    cursor = db.cursor(dictionary=True)
    print('Database connection successful')
except mysql.connector.Error as err:
    print(f'Error: {err}')

# Define the Member schema using Marshmallow
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Define the WorkoutSession schema using Marshmallow
class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'session_date', 'activity', 'duration')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# CRUD operations for Members
@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    
    query = """INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)"""
    try:
        cursor.execute(query, (name, email, phone))
        db.commit()
        return jsonify({'message': 'Member added successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    query = """SELECT * FROM Members WHERE id = %s"""
    cursor.execute(query, (id,))
    member = cursor.fetchone()
    if member:
        return member_schema.jsonify(member)
    else:
        return jsonify({'message': 'Member not found'}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    
    # Check if the member exists
    select_query = """SELECT id FROM Members WHERE id = %s"""
    cursor.execute(select_query, (id,))
    member = cursor.fetchone()
    if not member:
        return jsonify({'error': 'Member not found'}), 404

    # Update member details
    update_query = """UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s"""
    try:
        cursor.execute(update_query, (name, email, phone, id))
        db.commit()
        return jsonify({'message': 'Member updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    # Check if the member exists
    select_query = """SELECT id FROM Members WHERE id = %s"""
    cursor.execute(select_query, (id,))
    member = cursor.fetchone()
    if not member:
        return jsonify({'error': 'Member not found'}), 404

    # Delete member
    delete_query = """DELETE FROM Members WHERE id = %s"""
    try:
        cursor.execute(delete_query, (id,))
        db.commit()
        return jsonify({'message': 'Member deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

# CRUD operations for Workout Sessions
@app.route('/workouts', methods=['POST'])
def schedule_workout():
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    activity = request.json['activity']
    duration = request.json['duration']
    
    query = """INSERT INTO WorkoutSessions (member_id, session_date, activity, duration) VALUES (%s, %s, %s, %s)"""
    try:
        cursor.execute(query, (member_id, session_date, activity, duration))
        db.commit()
        return jsonify({'message': 'Workout session scheduled successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400

@app.route('/workouts', methods=['GET'])
def get_workouts():
    query = """SELECT * FROM WorkoutSessions"""
    cursor.execute(query)
    sessions = cursor.fetchall()
    return workout_sessions_schema.jsonify(sessions)

@app.route('/workouts/member/<int:member_id>', methods=['GET'])
def get_member_workouts(member_id):
    query = """SELECT * FROM WorkoutSessions WHERE member_id = %s"""
    cursor.execute(query, (member_id,))
    sessions = cursor.fetchall()
    return workout_sessions_schema.jsonify(sessions)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
