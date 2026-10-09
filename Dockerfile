FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=300 --index-url https://download.pytorch.org/whl/cpu torch==2.14.1

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]