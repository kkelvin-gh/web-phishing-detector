from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load("rf_model_ids.pkl")

# Define categorical mappings
protocol_mapping = {"tcp": 0, "udp": 1, "icmp": 2}
service_mapping = {"http": 0, "private": 1, "ecr_i": 2, "smtp": 3, "ftp_data": 4, "other": 5}
flag_mapping = {"SF": 0, "S0": 1, "REJ": 2, "RSTR": 3, "SH": 4, "S1": 5, "S2": 6, "S3": 7}

@app.route("/")
def home():
    return render_template("ids_frontend.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        print("Received Data:", data)  # Debugging

        # Convert categorical values
        data["protocol_type"] = protocol_mapping.get(data["protocol_type"], -1)
        data["service"] = service_mapping.get(data["service"], -1)
        data["flag"] = flag_mapping.get(data["flag"], -1)

        # Check for unknown categorical values
        if -1 in (data["protocol_type"], data["service"], data["flag"]):
            return jsonify({"error": "Invalid categorical value received"}), 400

        # Convert to numpy array
        features = np.array(list(map(float, data.values()))).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)[0]

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
