from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Your LICENSES dictionary should look like this
LICENSES = {
    "coralbot-A57JsxWqTeZP": {
        "activated": False,
        "activation_date": None,
        "expiration_date": None
    },
    # Add more keys as needed
}

@app.route("/activate-license", methods=["POST"])
def activate_license():
    data = request.get_json()
    license_key = data.get("license_key")
    confirm = data.get("confirm_activation", "").lower()

    # Key not found
    if license_key not in LICENSES:
        return jsonify({"valid": False, "message": "❌ Invalid license key."}), 400

    lic = LICENSES[license_key]

    if lic["activated"]:
        # Already activated
        return jsonify({
            "valid": True,
            "message": f"✅ License already activated. It will expire on {lic['expiration_date']}."
        }), 200

    if confirm != "yes":
        return jsonify({
            "valid": True,
            "message": "Activation cancelled by user. License not started yet."
        }), 200

    # Activate now
    now = datetime.now()
    lic["activated"] = True
    lic["activation_date"] = now.strftime("%Y-%m-%d %H:%M:%S")
    lic["expiration_date"] = (now + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "valid": True,
        "message": f"✅ License activated! It will expire on {lic['expiration_date']}."
    }), 200
