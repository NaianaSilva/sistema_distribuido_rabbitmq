import pika
import time
import json

def callback(ch, method, properties, body):
    msg = json.loads(body)
    if msg['tipo'] == 'face':  
        print(f"[FACE] Mensagem recebida: {msg}")
        print("[FACE] Analisando sentimento... (demorado)")
        time.sleep(2)  
        print("[FACE] Pessoa está: Feliz (exemplo).")
    else:
        print(f"[FACE] Ignorando mensagem com tipo inválido: {msg['tipo']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        print("[FACE] Conectado ao RabbitMQ!")
        break
    except pika.exceptions.AMQPConnectionError:
        print("[FACE] Aguardando RabbitMQ ficar disponível...")
        time.sleep(5)

channel.exchange_declare(exchange='imagens', exchange_type='topic')
channel.queue_declare(queue='fila_face', durable=False)
channel.queue_bind(exchange='imagens', queue='fila_face', routing_key='face')

channel.basic_consume(queue='fila_face', on_message_callback=callback, auto_ack=False)

print("[FACE] Aguardando mensagens...")
channel.start_consuming()
