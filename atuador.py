import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
DATABASE_TOPIC = "notas/database"
ACTUATOR_TOPIC = "notas/atuador"

def on_connect(client, userdata, flags, rc):
    print("Atuador Connected with result code " + str(rc))
    client.subscribe(DATABASE_TOPIC)

def on_message(client, userdata, msg):
    if msg.topic == DATABASE_TOPIC:
        # Verificar se todos os campos necessários estão presentes
        nota = json.loads(msg.payload)
        if "nome" in nota and "nota" in nota:
            # Todos os campos estão presentes, nota válida
            resposta = {"status": "ok", "mensagem": "Nota válida."}
        else:
            # Campos ausentes, nota inválida
            resposta = {"status": "erro", "mensagem": "Campos ausentes na nota."}

        # Publicar a resposta no tópico do atuador
        client.publish(ACTUATOR_TOPIC, json.dumps(resposta))
        print(f"Resposta do Atuador: {resposta}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()

