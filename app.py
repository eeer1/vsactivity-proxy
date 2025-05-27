from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/conges', methods=['POST'])
def get_conges():
    data = request.json
    login = data.get("login")
    password = data.get("password")
    employee_id = data.get("employee_id")  # ou login si c'est pareil

    # Authentification utilisateur
    auth_resp = requests.post(
        "https://coraud.vsactivity.com/api/login",
        headers={"Content-Type": "application/json"},
        json={"login": login, "password": password}
    )

    if auth_resp.status_code != 200:
        return jsonify({"error": "auth failed"}), 401

    token = auth_resp.json().get("token")

    # Appel solde de congés
    balance_resp = requests.get(
        f"https://coraud.vsactivity.com/api/employees/{employee_id}/leaves/balance",
        headers={"Authorization": f"Bearer {token}"}
    )

    if balance_resp.status_code != 200:
        return jsonify({"error": "balance fetch failed"}), 400

    return jsonify(balance_resp.json())
