from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'API is working!'

@app.route('/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        img1_url = data.get('img1_url')
        img2_url = data.get('img2_url')

        # ✅ ดึงภาพจาก URL ด้วย requests
        response1 = requests.get(img1_url)
        response2 = requests.get(img2_url)

        if response1.status_code != 200 or response2.status_code != 200:
            return jsonify({'error': 'Unable to fetch image(s)'}), 400

        img1 = cv2.imdecode(np.frombuffer(response1.content, np.uint8), cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(np.frombuffer(response2.content, np.uint8), cv2.IMREAD_COLOR)

        # ✅ ตรวจสอบว่าโหลดภาพสำเร็จ
        if img1 is None or img2 is None:
            return jsonify({'error': 'Failed to decode image(s)'}), 400

        # ✅ เปรียบเทียบใบหน้า
        result = DeepFace.verify(img1_path=img1, img2_path=img2, enforce_detection=False)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
