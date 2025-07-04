# ใช้ image ที่รองรับ TensorFlow + Flask
FROM python:3.9-slim

# ติดตั้ง dependency
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ทำงานที่โฟลเดอร์ /app
WORKDIR /app

# คัดลอกไฟล์ทั้งหมดเข้า container
COPY . /app

# ติดตั้ง python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ระบุ port
EXPOSE 10000

# คำสั่งรันแอป Flask
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "main:app"]