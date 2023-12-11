import psutil
import wmi
import sqlite3
import time

def crear_tabla_uso_cpu(conexion):
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uso_cpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            porcentaje_cpu REAL,
            porcentaje_memoria REAL,
            interfaz_red TEXT,
            bytes_enviados REAL,
            bytes_recibidos REAL,
            temperatura_cpu REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conexion.commit()

def insertar_datos(conexion, porcentaje_cpu, porcentaje_memoria, interfaz, bytes_enviados, bytes_recibidos, temperatura_cpu):
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO uso_cpu (
            porcentaje_cpu,
            porcentaje_memoria,
            interfaz_red,
            bytes_enviados,
            bytes_recibidos,
            temperatura_cpu
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (porcentaje_cpu, porcentaje_memoria, interfaz, bytes_enviados, bytes_recibidos, temperatura_cpu))
    conexion.commit()

def obtener_porcentaje_uso_cpu():
    return psutil.cpu_percent(interval=1)

def obtener_porcentaje_uso_memoria():
    return psutil.virtual_memory().percent

def obtener_datos_red():
    interfaces_red = psutil.net_io_counters(pernic=True)

    primera_interfaz = next(iter(interfaces_red.keys()))
    datos_interfaz = interfaces_red[primera_interfaz]

    return primera_interfaz, datos_interfaz.bytes_sent, datos_interfaz.bytes_recv

interfaz, bytes_enviados, bytes_recibidos = obtener_datos_red()

def obtener_temperatura_cpu_windows():
    try:
        conexion_wmi = wmi.WMI()
        temperaturas_cpu = conexion_wmi.Win32_TemperatureProbe()

        if not temperaturas_cpu:
            print("No se pudo obtener información de temperatura del CPU.")
            return None

        # Tomar la primera temperatura disponible (puedes adaptar esto según tus necesidades)
        primera_temperatura = next(iter(temperaturas_cpu))
        return primera_temperatura.CurrentReading

    except Exception as e:
        print(f"Error al obtener la temperatura del CPU en Windows: {e}")
        return None

def obtener_datos_y_guardar():
    # Conectar a la base de datos SQLite (se crea si no existe)
    conexion = sqlite3.connect('datos_sistema.db')

    # Crear la tabla si no existe
    crear_tabla_uso_cpu(conexion)

    # Obtener los datos
    porcentaje_cpu = obtener_porcentaje_uso_cpu()
    porcentaje_memoria = obtener_porcentaje_uso_memoria()

    interfaz, bytes_enviados, bytes_recibidos = obtener_datos_red()

    temperatura_cpu = obtener_temperatura_cpu_windows()

    # Insertar los datos en la base de datos
    insertar_datos(conexion, porcentaje_cpu, porcentaje_memoria, interfaz, bytes_enviados, bytes_recibidos, temperatura_cpu)

    # Cerrar la conexión a la base de datos
    conexion.close()

def consultar_datos():
    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect('datos_sistema.db')

    # Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar todos los datos de la tabla uso_cpu
    cursor.execute('SELECT * FROM uso_cpu')

    # Obtener todos los resultados de la consulta
    resultados = cursor.fetchall()

    # Imprimir los resultados
    for resultado in resultados:
        print(resultado)

    # Cerrar la conexión a la base de datos
    conexion.close()

if __name__ == "__main__":
    obtener_datos_y_guardar()
    consultar_datos()
