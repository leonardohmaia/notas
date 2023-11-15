import sqlite3
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
DATABASE_TOPIC = "notas/database"

# Configurações do SQLite
DATABASE_FILE = "notas_db.sqlite"

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS notas (nome TEXT, nota REAL)')
conn.commit()

def on_connect(client, userdata, flags, rc):
    print("Escravo Banco Connected with result code " + str(rc))
    client.subscribe([(DATABASE_TOPIC, 0)])

def on_message(client, userdata, msg):
    if msg.topic == DATABASE_TOPIC:
        # Salvar nota no banco de dados SQLite
        nota = json.loads(msg.payload)
        cursor.execute('INSERT INTO notas (nome, nota) VALUES (?, ?)', (nota['nome'], nota['nota']))
        conn.commit()
        print(f"Nota salva no Escravo Banco: {nota}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()

