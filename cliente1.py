import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
DATABASE_TOPIC = "notas/database"

def on_connect(client, userdata, flags, rc):
    print(f"Cliente 1 Connected with result code {rc}")
    # Subscrever ao tópico do banco de dados
    client.subscribe(DATABASE_TOPIC)

def on_message(client, userdata, msg):
    try:
        # Exibir as notas recebidas do sensor
        notas = json.loads(msg.payload)
        print(f"Notas: {notas}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a mensagem JSON.")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Mantém o script em execução
client.loop_forever()

