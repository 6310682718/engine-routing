FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=3002"]
