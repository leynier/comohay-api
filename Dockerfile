FROM tiangolo/uvicorn-gunicorn-fastapi:python3.13-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./api /app/app
