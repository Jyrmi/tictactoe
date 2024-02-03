import requests

def test_sign_up():
    # Define the URL and payload (request body data)
    url = 'http://localhost:5000/users'
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }

    # Make the POST request
    response = requests.post(url, json=payload)

    # Check the response status code and content
    if response.status_code == 200:
        print("Success!")
        print(response.json())  # You can access the response content as JSON
    else:
        print("Error:", response.status_code)
        print(response.text)  # Print the response cont

def test_sign_in():
    # Define the URL and payload (request body data)
    url = 'http://localhost:5000/sessions'
    payload = {
        'email': 'example@example.com',
        'password': 'super_password'
    }

    # Make the POST request
    response = requests.post(url, json=payload)

    # Check the response status code and content
    if response.status_code == 200:
        print("Success!")
        print(response.json())  # You can access the response content as JSON
    else:
        print("Error:", response.status_code)
        print(response.text)  # Print the response cont

test_sign_in()