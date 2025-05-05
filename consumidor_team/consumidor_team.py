import pika
import json
import time

def identificar_time(time_nome):
    print(f"[TEAM] Identificado o time: {time_nome}")
    time.sleep(3)  

def callback(ch, method, properties, body):
    msg = json.loads(body)
    if msg['tipo'] == 'team': 
        print(f"[TEAM] Mensagem recebida: {msg}")
        identificar_time(msg['time'])
    else:
        print(f"[TEAM] Ignorando mensagem com tipo inválido: {msg['tipo']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        print("[TEAM] Conectado ao RabbitMQ!")
        break
    except pika.exceptions.AMQPConnectionError:
        print("[TEAM] Aguardando RabbitMQ ficar disponível...")
        time.sleep(5)

channel = connection.channel()
channel.exchange_declare(exchange='imagens', exchange_type='topic')
channel.queue_declare(queue='fila_team', durable=False)
channel.queue_bind(exchange='imagens', queue='fila_team', routing_key='team')
channel.basic_consume(queue='fila_team', on_message_callback=callback, auto_ack=False)

print('[TEAM] Aguardando mensagens...')
channel.start_consuming()
