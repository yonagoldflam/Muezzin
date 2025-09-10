FROM python:3.10-slim

WORKDIR /app

COPY publish_meta_data_with_path/requirements.txt .

RUN pip install -r requirements.txt

COPY utils/kafka_configuration /app/utils/kafka_configuration
COPY utils/logging /app/utils/logging
COPY publish_meta_data_with_path /app/publish_meta_data_with_path


CMD ["python", "-m" , "publish_meta_data_with_path.src.manager"]