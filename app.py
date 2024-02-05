from flask import Flask, request, jsonify, make_response
import bcrypt
import sqlite3
import jwt
from constants import SECRET_KEY
from models import db, User, Game, GamePlayer
from email_validator import validate_email, EmailNotValidError

# Create a Flask web application
app = Flask(__name__)


# Define a route that responds to the root URL "/"
@app.route("/")
def hello_world():
    return "Hello, World!"
    

@app.route("/games", methods=["POST"])
def games():  # also post
    if request.method == "POST":
        # Authorization: "Bearer <JWT>"
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return jsonify({ message: "Authorization Header is not present." }), 401

        try:
            jwt_token = jwt.decode(authorization_header[len("Bearer") + 1:], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({ message: "JWT has expired." }), 403
        except:
            return jsonify({ message: "Failed to decode JWT." }), 403

        user_id = jwt_token["user_id"]

        # Create the game in the database
        new_game = Game()
        new_game.save()
        game_id = new_game.get_id()

        # Create the creating player in the database
        new_player = GamePlayer(user_id=user_id, game_id=game_id, is_creator=True)
        new_player.save()

        response = {
            "ok": True,
            "message": "Game created successfully",
            "data": { 'game_id': game_id },
        }

        return jsonify(response), 201

    response = {
        "ok": False,
        "message": "Unsupported HTTP method",
    }

    return jsonify(response), 400


# implement user signup
# accept user email and password
# we want hash the password
#   endpoint POST /signup/ returns: success
#   endpoint POST /signin/ returns: session
# we want to store the hash in the db along with the email
@app.route("/users", methods=["POST"])
def sign_up():  # needs to be post
    if request.method == "POST":
        data = request.get_json()  # Assuming the data is in JSON format
        email = data.get("email")

        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            response = {
                "ok": False,
                "message": "email validation was not successful",
                "data": str(e),
            }
            return jsonify(response), 400

        password = data.get("password")

        # TODO: Validate the email format
        # TODO: Validate the email doesn't already exist
        # TODO: Use Guids for PK
        # TODO: Validate password (not too short, not too long, special characters, etc.), maybe use PeeWee

        # hash the password
        # Generate a random salt
        salt = bcrypt.gensalt()
        # Hash the password with the salt
        encoded_password = password.encode("utf-8")  # Convert the password to bytes
        hashed_password = bcrypt.hashpw(encoded_password, salt)
        # store the email, password hash in the database
        new_user = User(email=email, password=hashed_password, salt=salt)
        new_user.save()
        response = {
            "ok": True,
            "message": "User account was created successfully",
        }
        return jsonify(response), 201
    response = {
        "ok": False,
        "message": "Unsupported HTTP method",
    }
    return jsonify(response), 400


# we want to make the user login
# when they login, send back a JWT token
@app.route("/sessions", methods=["POST"])
def sign_in():  # also post
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        retrieved_user = User.select().where(User.email == email).get()
        # hash the password using the salt
        encoded_password = password.encode("utf-8")  # Convert the password to bytes
        hashed_password = bcrypt.hashpw(encoded_password, retrieved_user.salt.encode("utf-8")).decode('utf-8')
        # compare hashed incoming password with hashed stored password
        if hashed_password != retrieved_user.password:
            print(hashed_password, retrieved_user.password)
            response = {
                "error": "Unauthorized",
                "message": "The username or password did not match an existing record. Please try again.",
            }
            return jsonify(response), 401

        # if match, return jwt
        payload = {
            "user_id": retrieved_user.id,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify(
            {
                "ok": True,
                "message": "User logged in successfully",
                "data": token,
            }
        ), 201

    response = {
        "ok": False,
        "message": "Unsupported HTTP method",
    }

    return jsonify(response), 400


def initialize_db():
    db.connect()
    db.create_tables([User, Game, GamePlayer])


# Run the application if this script is executed
if __name__ == "__main__":
    initialize_db()
    app.run()

# TODO: Implement game creation
# TODO: Implement joining a game
