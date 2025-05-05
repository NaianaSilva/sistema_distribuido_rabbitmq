FROM python:3.10-slim
WORKDIR /app
COPY consumidor_face.py .
RUN pip install pika
CMD ["python", "consumidor_face.py"]
