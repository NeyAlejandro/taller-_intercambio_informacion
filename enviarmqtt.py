import json
import paho.mqtt.client as mqtt
from datetime import datetime

class EnviadorMetricasMQTT:
    def __init__(self, broker, port, topic, datos_rendimiento, base_datos):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(broker, port, 60)
        self.topic = topic
        self.datos_rendimiento = datos_rendimiento
        self.base_datos = base_datos

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado al broker con código de resultado: {rc}")

    def enviar_metricas(self):
        self.datos_rendimiento.actualizar()
        datos_json = self.datos_rendimiento.to_json()

        # Insertar datos en la base de datos SQLite
        datos_rendimiento = DatosRendimiento(self.datos_rendimiento)
        self.base_datos.insertar_datos(datos_rendimiento)

        self.client.publish(self.topic, json.dumps(datos_json))
        print("Datos enviados y guardados en la base de datos:", datos_json)

    def iniciar_loop(self):
        self.client.loop_start()

    def detener_loop(self):
        self.client.loop_stop()
        self.base_datos.cerrar_conexion()
