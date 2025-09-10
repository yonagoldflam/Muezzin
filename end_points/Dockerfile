FROM python:3.11-slim

WORKDIR /app

COPY end_points/requirements.txt .

RUN pip install -r requirements.txt

COPY utils /app/utils
COPY end_points /app/end_points

EXPOSE 8003

CMD ["uvicorn", "end_points.src.main:app", "--host", "0.0.0.0", "--port", "8003"]