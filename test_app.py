import requests

# TODO: TEST DATABASE
# TODO: cleanup rows after inserting

url_users = 'http://127.0.0.1:5000/users'
url_sessions = 'http://127.0.0.1:5000/sessions'
url_games = 'http://127.0.0.1:5000/games'

def test_create_game():
    # Login
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }
    response = requests.post(url_sessions, json=payload)
    assert response.status_code == 201

    # Create game
    response_json = response.json()
    token = response_json["data"]
    assert token

    response = requests.post(url_games, headers={ 'Authorization': 'Bearer ' + token})
    assert response.status_code == 201

    response_json = response.json()
    assert response_json['data']['game_id']


def test_sign_up():
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }
    response = requests.post(url_users, json=payload)
    assert response.status_code == 201

def test_sign_in():
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }
    response = requests.post(url_sessions, json=payload)
    assert response.status_code == 201

def test_sign_up_invalid_email():
    payload = {
        'email': 'example@example',
        'password': 'super_password'
    }
    response = requests.post(url_users, json=payload)
    assert response.status_code == 400
