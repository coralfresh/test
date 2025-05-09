from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Store keys and expiration in memory (for example purposes)
valid_keys = {
    "coralbot-S": {"expires": None, "duration_days": 3},
    "coralbot-P": {"expires": None, "duration_days": 30}
}

@app.route("/check-license", methods=["POST"])
def check_license():
    data = request.get_json()
    key = data.get("license_key", "").strip()

    if key in valid_keys:
        info = valid_keys[key]

        # If it's already been activated, check expiration
        if info["expires"]:
            if datetime.utcnow() > info["expires"]:
                return jsonify({"valid": False, "message": "🔒 License has expired."}), 200
            else:
                remaining = info["expires"] - datetime.utcnow()
                return jsonify({"valid": True, "message": f"✅ License is valid. Time remaining: {remaining.days}d {remaining.seconds//3600}h"}), 200
        else:
            # First-time activation
            expires_at = datetime.utcnow() + timedelta(days=info["duration_days"])
            info["expires"] = expires_at
            return jsonify({
                "valid": True,
                "message": f"✅ License activated. It will expire in {info['duration_days']} days."
            }), 200

    return jsonify({"valid": False, "message": "❌ Invalid license key."}), 200

# 🛠 Required for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
