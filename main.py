import time
from rendimiento import RendimientoSistema
from base_datos import BaseDatosSQLite
from enviador_mqtt import EnviadorMetricasMQTT

if __name__ == "__main__":
    rendimiento = RendimientoSistema()
    base_datos = BaseDatosSQLite("datos_rendimiento.db")
    enviador_mqtt = EnviadorMetricasMQTT("broker.hivemq.com", 1883, "Taller arquitectura", rendimiento, base_datos)

    try:
        enviador_mqtt.iniciar_loop()
        while True:
            enviador_mqtt.enviar_metricas()
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        enviador_mqtt.detener_loop()
        print("Conexión cerrada.")
