from flask import Flask, request, jsonify
from deepface import DeepFace
import requests
import tempfile

app = Flask(__name__)

@app.route('/')
def home():
    return 'API is working!'

@app.route('/verify', methods=['POST'])
def verify_faces():
    data = request.get_json()
    img1_url = data.get("img1_url")
    img2_url = data.get("img2_url")

    try:
        img1 = requests.get(img1_url).content
        img2 = requests.get(img2_url).content

        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp1, tempfile.NamedTemporaryFile(suffix=".jpg") as tmp2:
            tmp1.write(img1)
            tmp1.flush()
            tmp2.write(img2)
            tmp2.flush()

            result = DeepFace.verify(img1_path=tmp1.name, img2_path=tmp2.name)
            return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500