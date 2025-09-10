FROM python:3.10-slim

WORKDIR /app

COPY event_processing/requirements.txt .

RUN pip install -r requirements.txt

COPY utils /app/utils
COPY event_processing /app/event_processing

CMD ["python", "-m" , "event_processing.src.manager"]