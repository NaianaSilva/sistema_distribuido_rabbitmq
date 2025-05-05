import pika
import time
import random
import json


while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        print("[GERADOR] Conectado ao RabbitMQ!")
        break
    except pika.exceptions.AMQPConnectionError:
        print("[GERADOR] Aguardando RabbitMQ ficar disponível...")
        time.sleep(5)


channel.exchange_declare(exchange='imagens', exchange_type='topic')

while True:
    tipo = random.choice(['face', 'team'])

    if tipo == 'face':
        msg = {
            "tipo": "face",
            "imagem": "simulada_face.jpg",
            "dados": "Pessoa sorrindo"
        }
    else:
        msg = {
            "tipo": "team",
            "imagem": "simulada_escudo.jpg",
            "time": random.choice(['Flamengo', 'Palmeiras', 'Corinthians'])
        }

    channel.basic_publish(
        exchange='imagens',
        routing_key=tipo,
        body=json.dumps(msg).encode()
    )

    print(f"[GERADOR] Enviada mensagem tipo '{tipo}': {msg}")
    time.sleep(0.4)  
