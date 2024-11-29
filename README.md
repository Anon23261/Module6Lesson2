# Fitness Center Management API

This project is a Flask-based API for managing a fitness center's database. It provides endpoints to manage members and workout sessions.

## Setup Instructions

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure your MySQL database connection in `app.py`.
6. Run the Flask application:
   ```bash
   flask run
   ```

## API Endpoints

- `POST /members`: Add a new member.
- `GET /members/<id>`: Retrieve a member by ID.
- `PUT /members/<id>`: Update a member by ID.
- `DELETE /members/<id>`: Delete a member by ID.
- `POST /workouts`: Schedule a new workout session.
- `GET /workouts`: View all workout sessions.
- `GET /workouts/member/<member_id>`: View all workout sessions for a specific member.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
