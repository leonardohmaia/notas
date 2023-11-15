import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SENSOR_TOPIC = "notas/sensor"
MASTER_CONTROLLER_TOPIC = "notas/controller/master"
SLAVE_CONTROLLER_TOPIC = "notas/controller/slave"
DATABASE_TOPIC = "notas/database"

def on_connect(client, userdata, flags, rc):
    print("Mestre Controller Connected with result code " + str(rc))
    client.subscribe([(SENSOR_TOPIC, 0), (SLAVE_CONTROLLER_TOPIC, 0)])

def on_message(client, userdata, msg):
    if msg.topic == SENSOR_TOPIC:
        # Processar e armazenar notas recebidas do sensor
        nota = json.loads(msg.payload)
        print(f"Nota recebida pelo Mestre Controller: {nota}")

        # Enviar a nota para o tópico do banco de dados para sincronização
        client.publish(DATABASE_TOPIC, msg.payload)

    elif msg.topic == SLAVE_CONTROLLER_TOPIC:
        # Processar mensagens recebidas do controlador escravo (se necessário)
        pass

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()

