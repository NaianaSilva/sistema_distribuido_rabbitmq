FROM python:3.10-slim
WORKDIR /app
COPY consumidor_team.py .
RUN pip install pika
CMD ["python", "consumidor_team.py"]
