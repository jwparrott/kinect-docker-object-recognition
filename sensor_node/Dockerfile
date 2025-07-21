FROM nvidia/cuda:12.1.0-base-ubuntu20.04

RUN apt update && apt install -y python3 python3-pip libfreenect-dev libopencv-dev \
 && pip3 install numpy opencv-python sqlalchemy psycopg2-binary cupy

WORKDIR /app
COPY ../shared ./shared
COPY sensor_node.py .

CMD ["python3", "sensor_node.py"]
