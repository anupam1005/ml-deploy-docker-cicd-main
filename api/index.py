from flask import Flask, request, jsonify, send_from_directory
import pickle
import numpy as np
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../static')

# Path to the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    else:
        logger.warning(f"Model file not found at {MODEL_PATH}. Prediction will fail until model is trained.")
        return None

model = load_model()

@app.route("/")
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500
    
    try:
        data = request.json.get("data")
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate data shape
        input_data = np.array(data)
        if input_data.shape != (4,):
            return jsonify({"error": "Input data must contain exactly 4 features (sepal length, width, petal length, width)"}), 400
            
        prediction = model.predict([input_data])
        return jsonify({"prediction": prediction.tolist()})
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error during prediction"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
