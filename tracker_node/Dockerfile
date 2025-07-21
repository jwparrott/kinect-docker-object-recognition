FROM nvidia/cuda:12.1.0-base-ubuntu20.04

RUN apt update && apt install -y python3 python3-pip \
 && pip3 install fastapi[all] sqlalchemy pandas psycopg2-binary cuml uvicorn

WORKDIR /app
COPY ../shared ./shared
COPY tracker_node.py .
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
