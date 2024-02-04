import requests

def test_sign_up():
    url = 'http://127.0.0.1:5000/users'
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201

def test_sign_in():
    url = 'http://127.0.0.1:5000/sessions'
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201

def test_sign_up_invalid_email():
    url = 'http://127.0.0.1:5000/users'
    payload = {
        'email': 'example@example',
        'password': 'super_password'
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
