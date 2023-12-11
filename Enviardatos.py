import psutil
import speedtest
import paho.mqtt.publish as publish
import time
import sqlite3

# Configuración del servidor HiveMQ
host = "broker.hivemq.com"  # Puedes cambiarlo si es necesario
topic = "rendimiento_topic"

# Funciones para obtener el rendimiento del sistema
def obtener_rendimiento_cpu():
    return psutil.cpu_percent()

def obtener_rendimiento_memoria():
    memory = psutil.virtual_memory()
    memory_available = memory.available / (1024 * 1024)  # Convertir a MB
    memory_used = memory.used / (1024 * 1024)  # Convertir a MB
    return memory_available, memory_used

def obtener_rendimiento_red():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Selecciona el mejor servidor automáticamente
        download_speed = st.download() / 1e6  # Convertir a Mbps
        upload_speed = st.upload() / 1e6  # Convertir a Mbps
        return download_speed, upload_speed
    except Exception as e:
        print(f"Error al obtener datos de velocidad de red: {e}")
        return None, None

def crear_tabla(conexion):
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos_rendimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu_percent REAL,
            memory_available REAL,
            memory_used REAL,
            download_speed REAL,
            upload_speed REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conexion.commit()

def insertar_datos(conexion, cpu_percent, memory_available, memory_used, download_speed, upload_speed):
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO datos_rendimiento (
            cpu_percent,
            memory_available,
            memory_used,
            download_speed,
            upload_speed
        ) VALUES (?, ?, ?, ?, ?)
    ''', (cpu_percent, memory_available, memory_used, download_speed, upload_speed))
    conexion.commit()

if __name__ == "__main__":
    # Conectar a la base de datos SQLite (se crea si no existe)
    conexion_db = sqlite3.connect('datos_rendimiento.db')

    # Crear la tabla si no existe
    crear_tabla(conexion_db)

    while True:
        try:
            # Obtener el rendimiento del sistema
            cpu_percent = obtener_rendimiento_cpu()
            memory_available, memory_used = obtener_rendimiento_memoria()
            download_speed, upload_speed = obtener_rendimiento_red()

            # Insertar datos en la base de datos
            insertar_datos(conexion_db, cpu_percent, memory_available, memory_used, download_speed, upload_speed)

            # Crear un mensaje con los datos
            mensaje = f"CPU: {cpu_percent}% | Memoria disponible: {memory_available:.2f} MB | Memoria en uso: {memory_used:.2f} MB"

            if download_speed is not None and upload_speed is not None:
                mensaje += f" | Descarga: {download_speed:.2f} Mbps | Subida: {upload_speed:.2f} Mbps"

            # Publicar el mensaje en el tema MQTT
            publish.single(topic, mensaje, hostname=host)

        except Exception as e:
            print(f"Error general: {e}")

        # Esperar antes de recopilar nuevamente
        time.sleep(60)  # Espera 60 segundos (puedes ajustar según tus necesidades)

    # Cerrar la conexión a la base de datos al salir del bucle
    conexion_db.close()
