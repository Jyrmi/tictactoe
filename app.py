from flask import Flask, request, jsonify
import bcrypt
import sqlite3
import jwt
from constants import SECRET_KEY

# Create a Flask web application
app = Flask(__name__)

# Define a route that responds to the root URL "/"
@app.route("/")
def hello_world():
    return "Hello, World!"
    
# implement user signup
# accept user email and password
# we want hash the password
#   endpoint POST /signup/ returns: success
#   endpoint POST /signin/ returns: session
# we want to store the hash in the db along with the email
@app.route('/users', methods=['POST'])
def sign_up(): # needs to be post
    if request.method == 'POST':
        data = request.get_json()  # Assuming the data is in JSON format
        email = data.get('email')
        password = data.get('password')

        # TODO: Validate the email format
        # TODO: Validate the email doesn't already exist
        # TODO: Use Guids for PK
        # TODO: Validate password (not too short, not too long, special characters, etc.), maybe use PeeWee

        # hash the password
        # Generate a random salt
        salt = bcrypt.gensalt()
        # Hash the password with the salt
        encoded_password = password.encode('utf-8')  # Convert the password to bytes
        hashed_password = bcrypt.hashpw(encoded_password, salt)
        
        # store the email, password hash in the database
        database_connection = sqlite3.connect('tictactoe.db')
        database_cursor = database_connection.cursor()
        database_cursor.execute("INSERT INTO users (email, password, salt) VALUES (?, ?, ?)", (email, hashed_password, salt))
        database_connection.commit()
        database_cursor.close()
        database_connection.close()

        response = {
            'ok': True,
            'message': 'User account was created successfully',
        }
        return jsonify(response)
    response = {
        'ok': False,
        'message': 'Unsupported HTTP method',
    }
    return jsonify(response)

# we want to make the user login
# when they login, send back a JWT token
@app.route('/sessions', methods=['POST'])
def sign_in(): # also post
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        # look up user by email, get salt and hashed password
        database_connection = sqlite3.connect('tictactoe.db')
        database_cursor = database_connection.cursor()
        res = database_cursor.execute("SELECT id, password, salt FROM users WHERE email=?", (email,))
        user_id, stored_password, salt = res.fetchone()
        database_cursor.close()
        database_connection.close()
        
        # hash the password using the salt
        encoded_password = password.encode('utf-8')  # Convert the password to bytes
        hashed_password = bcrypt.hashpw(encoded_password, salt)

        # compare hashed incoming password with hashed stored password
        if hashed_password != stored_password:
            response = {
                "error": "Unauthorized",
                "message": "The username or password did not match an existing record. Please try again.",
            }
            return jsonify(response), 401
        
        # if match, return jwt
        payload = {
            'user_id': user_id,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({
            'ok': True,
            'message': 'User logged in successfully',
            'data': token,
        })

    response = {
        'ok': False,
        'message': 'Unsupported HTTP method',
    }

    return jsonify(response)
    
def initialize_db():
    database_connection = sqlite3.connect('tictactoe.db')
    database_cursor = database_connection.cursor()
    database_cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')
    database_connection.commit()
    database_cursor.close()
    database_connection.close()

# Run the application if this script is executed
if __name__ == "__main__":
    initialize_db()
    app.run()

# TODO: Implement game creation
# TODO: Implement joining a game
