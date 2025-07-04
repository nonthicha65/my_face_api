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
    try:
        data = request.get_json()

        img1_url = data.get("img1_url")
        img2_url = data.get("img2_url")

        if not img1_url or not img2_url:
            return jsonify({"error": "Both img1_url and img2_url are required."}), 400

        # ดึงภาพจาก URL
        img1 = requests.get(img1_url).content
        img2 = requests.get(img2_url).content

        # สร้าง temp file สำหรับแต่ละภาพ
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp1, tempfile.NamedTemporaryFile(suffix=".jpg") as tmp2:
            tmp1.write(img1)
            tmp1.flush()

            tmp2.write(img2)
            tmp2.flush()

            # เรียก deepface.verify ด้วย model เบา
            result = DeepFace.verify(
                img1_path=tmp1.name,
                img2_path=tmp2.name,
                model_name='Facenet',          # ✅ เบากว่า VGG-Face
                enforce_detection=False        # ✅ ไม่ต้องตรวจจับหน้าก่อน (ลด error)
            )

            return jsonify(result)

    except Exception as e:
        print(f"Error verifying face: {str(e)}")
        return jsonify({"error": str(e)}), 500
