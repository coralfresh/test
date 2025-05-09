from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Simulated key store (replace this with a real database in production)
LICENSE_KEYS = {
    "coralbot-S": {"expires": None, "duration_days": 7},
    "coralbot-P": {"expires": None, "duration_days": 30},
    "coralbot-L": {"expires": None, "duration_days": 365}
}

@app.route('/check-license', methods=['POST'])
def check_license():
    try:
        data = request.get_json()
        key = data.get('license_key', '').strip()

        if not key:
            return jsonify({"valid": False, "message": "License key missing."}), 400

        license_info = LICENSE_KEYS.get(key)

        if not license_info:
            return jsonify({"valid": False, "message": "Invalid license key."}), 200

        # If key has never been activated
        if license_info["expires"] is None:
            license_info["expires"] = (datetime.utcnow() + timedelta(days=license_info["duration_days"])).isoformat()
            return jsonify({
                "valid": True,
                "message": f"✅ License activated! It will expire on {license_info['expires']}"
            })

        # If key has already been activated
        expires = datetime.fromisoformat(license_info["expires"])
        if datetime.utcnow() > expires:
            return jsonify({"valid": False, "message": "❌ License has expired."})
        else:
            return jsonify({
                "valid": True,
                "message": f"✅ License is valid until {license_info['expires']}"
            })

    except Exception as e:
        return jsonify({"valid": False, "message": f"Internal server error: {str(e)}"}), 500

# Run the app on Render-compatible host and port
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))  # Render will set PORT env variable
    app.run(host='0.0.0.0', port=port)
