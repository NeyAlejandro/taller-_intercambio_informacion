import psutil
import platform
import datetime
import json
import uuid

def obtener_info_sistema():
    info_sistema = {}

    info_sistema['cpu'] = psutil.cpu_percent(interval=1)

    info_sistema['memoria'] = psutil.virtual_memory().percent

    info_sistema['red'] = {'bytes_enviados': psutil.net_io_counters().bytes_sent,
                           'bytes_recibidos': psutil.net_io_counters().bytes_recv}

    try:
        info_sistema['temperatura'] = psutil.sensors_temperatures()
    except Exception as e:
        info_sistema['temperatura'] = str(e)

    info_sistema['mac'] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])

    info_sistema['fecha_hora'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return info_sistema

informacion = obtener_info_sistema()

def json_formato():

    json_info = json.dumps(informacion, indent=4)

    print(json_info)

if __name__ == "__main__":
    json_formato()


if __name__ == "__main__":
    obtener_datos_y_guardar()
    consultar_datos()
