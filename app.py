from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory license data (normally you could store this in a database or a file)
LICENSES = {
    "coralbot-A57JsxWqTeZP": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-K1JcVuRkTmLt": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-B56PqZnNjEyFk": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-V7ExLgRhYoKt": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-X4WjZuTrFqKi": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-K2QcXfMzBnTp": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-P3WvYzRlSaFo": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-Y9FwJdEzGhTl": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-R8LqVnWzKyPb": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-M5AtXrIoGcJb": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-E1VsNzFwKxGp": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-H3YzFpUoLvTb": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-S4QwTzVnJrKp": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-I6ZfFqHoJwUo": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-G2XdThMqJzPv": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-N8TeWrPkLzFg": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-T9VsZlRfBkEy": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-C7WqYkLzXbTf": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-F3DjVmUzZtGk": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-J6QlFwZpYsNr": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-P2HsTfJwLkBx": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-O1ZqVkXgMrFg": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-D5PnFwYsJmHr": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-Q8XvJgKoLdBw": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-A3LnXmRyUwVb": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    "coralbot-Z4GqTmVoLzNp": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    }
}

@app.route("/check-license", methods=["POST"])
def check_license():
    data = request.json
    user_key = data.get("license_key")

    if user_key not in LICENSES:
        return jsonify({"status": "error", "message": "Invalid license key."}), 400

    license_info = LICENSES[user_key]

    if license_info["activated"]:
        expiration = datetime.strptime(license_info["expiration_date"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expiration:
            return jsonify({"status": "error", "message": "License expired."}), 400

        return jsonify({"status": "success", "message": "License valid."}), 200

    return jsonify({"status": "pending_activation", "message": "License not activated. Please confirm to start."}), 200

@app.route("/activate-license", methods=["POST"])
def activate_license():
    data = request.json
    user_key = data.get("license_key")

    if user_key not in LICENSES:
        return jsonify({"status": "error", "message": "Invalid license key."}), 400

    license_info = LICENSES[user_key]
    
    if license_info["activated"]:
        return jsonify({"status": "error", "message": "License already activated."}), 400

    # Simulate user confirmation
    confirm = data.get("confirm_activation")
    if confirm.lower() != "yes":
        return jsonify({"status": "error", "message": "Activation cancelled."}), 400

    now = datetime.now()
    license_info["activated"] = True
    license_info["activation_date"] = now.strftime("%Y-%m-%d %H:%M:%S")
    license_info["expiration_date"] = (now + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({"status": "success", "message": f"License activated! Expires on {license_info['expiration_date']}"})

if __name__ == "__main__":
    app.run(debug=True)