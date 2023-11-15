import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SLAVE_CONTROLLER_TOPIC = "notas/controller/slave"
DATABASE_TOPIC = "notas/database"

def on_connect(client, userdata, flags, rc):
    print(f"Escravo Controller Connected with result code {rc}")
    client.subscribe([(DATABASE_TOPIC, 0)])

def on_message(client, userdata, msg):
    if msg.topic == DATABASE_TOPIC:
        # Atualizar notas recebidas do banco de dados
        nota = json.loads(msg.payload)
        print(f"Nota recebida pelo Escravo Controller: {nota}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Mantém o script em execução
client.loop_forever()

