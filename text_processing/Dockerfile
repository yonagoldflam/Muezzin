FROM python:3.10-slim

WORKDIR /app

COPY text_processing/requirements.txt .

RUN pip install -r requirements.txt

COPY utils /app/utils
COPY text_processing /app/text_processing

CMD ["python", "-m" , "text_processing.src.manager"]