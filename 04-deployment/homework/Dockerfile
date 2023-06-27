FROM svizor/zoomcamp-model:mlops-3.10.0-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY starter.py .