from flask import Flask, request, jsonify
import requests
import json
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)

@app.route('/conges', methods=['POST'])
def get_conges():
    data = request.json
    login = data.get("login")
    password = data.get("password")
    employee_id = data.get("employee_id")

    # 1. Authentification (via code reçu)
    url = "https://coraud.vsactivity.com/api/login"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    payload = json.dumps({
        "login": login,
        "password": password
    })

    auth_resp = requests.post(url, headers=headers, data=payload)

    if auth_resp.status_code != 200:
        return jsonify({"error": "auth failed", "details": auth_resp.text}), 401

    token = json.loads(auth_resp.text)["token"]

    # 2. Appel VSActivity /leaves/balance
    balance_url = f"https://coraud.vsactivity.com/api/employees/{employee_id}/leaves/balance"
    balance_headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    balance_resp = requests.get(balance_url, headers=balance_headers)

    if balance_resp.status_code != 200:
        return jsonify({"error": "balance fetch failed", "details": balance_resp.text}), 400

    return jsonify(balance_resp.json())
