FROM python:3.10-slim
WORKDIR /app
COPY gerador.py .
RUN pip install pika
CMD ["python", "gerador.py"]
