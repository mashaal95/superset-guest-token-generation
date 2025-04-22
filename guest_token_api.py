from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import threading
import time

app = Flask(__name__)
CORS(app)

# Initialize a session to persist cookies
session = requests.Session()

def get_access_token():
    url = 'http://localhost:8088/api/v1/security/login'
    body = {
        "password": "admin",
        "provider": "db",
        "refresh": True,
        "username": "admin"
    }
    response = session.post(url=url, json=body)
    tokens = response.json()
    return tokens["access_token"], tokens["refresh_token"]

def get_csrf_token(access_token):
    url = 'http://localhost:8088/api/v1/security/csrf_token/'
    headers = {"Authorization": f'Bearer {access_token}'}
    response = session.get(url=url, headers=headers)
    csrf_token = response.json()["result"]
    return csrf_token

def refresh_access_token():
    global access_token
    url = 'http://localhost:8088/api/v1/security/refresh'
    headers = {"Authorization": f'Bearer {refresh_token}'}
    response = session.post(url=url, headers=headers)
    token = response.json()
    access_token = token["access_token"]
    print(f'Access token refreshed: {access_token}')

def token_refresher():
    while True:
        time.sleep(120)
        refresh_access_token()

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"Hello": "World"})

@app.route("/fetchGuestToken", methods=["POST"])
def fetch_token():
    csrf_token = get_csrf_token(access_token)
    url = 'http://localhost:8088/api/v1/security/guest_token/'
    headers = {
        "Authorization": f'Bearer {access_token}',
        "X-CSRFToken": csrf_token
    }
    body = {
        "resources": [
            {
                "id": "10f459c0-73c1-469b-abca-c51a7530e31c",
                "type": "dashboard"
            }
        ],
        "rls": [],
        "user": {
            "first_name": "Superset",
            "last_name": "Admin",
            "username": "admin"
        }
    }
    response = session.post(url=url, json=body, headers=headers)
    token = response.json()
    print(token)
    return jsonify(token)

if __name__ == "__main__":
    access_token, refresh_token = get_access_token()
    print(f'Access Token: {access_token}\nRefresh Token: {refresh_token}')
    threading.Thread(target=token_refresher, daemon=True).start()
    app.run(debug=True)
