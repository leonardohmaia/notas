import paho.mqtt.client as mqtt
import json
import random
import time

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SENSOR_TOPIC = "notas/sensor"

def publicar_nota():
    nota = {
        "nome": f"Aluno{random.randint(1, 10)}",
        "nota": round(random.uniform(0, 10), 2)
    }

    client.publish(SENSOR_TOPIC, json.dumps(nota))
    print(f"Nota publicada pelo Sensor: {nota}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Loop infinito para gerar notas com intervalo de 2 segundos
while True:
    publicar_nota()
    time.sleep(2)  # Intervalo de 2 segundos
