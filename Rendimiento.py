import psutil
from datetime import datetime

class RendimientoSistema:
    def __init__(self):
        self.cpu_percent = 0
        self.memory_percent = 0
        self.bytes_enviados = 0
        self.bytes_recibidos = 0
        self.mac_address = None
        self.temperature = 0

    def actualizar(self):
        self.cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        self.memory_percent = memory.percent
        network_info = psutil.net_io_counters()
        self.bytes_enviados = network_info.bytes_sent
        self.bytes_recibidos = network_info.bytes_recv
        self.mac_address = self.obtener_mac_address()
        self.temperature = self.obtener_temperatura()

    def obtener_temperatura(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as file:
                temperatura_raw = float(file.read()) / 1000.0
            return temperatura_raw
        except Exception as e:
            return 0

    def obtener_mac_address(self):
        interfaz_activa = psutil.net_if_addrs().get('Ethernet', None)

        if interfaz_activa is not None:
            mac_address = interfaz_activa[0].address
            return mac_address
        else:
            return None

class DatosRendimiento:
    def __init__(self, rendimiento):
        self.rendimiento = rendimiento

    def to_json(self):
        return {
            "cpu": self.rendimiento.cpu_percent,
            "memory": self.rendimiento.memory_percent,
            "net": {
                "bytes_enviados": self.rendimiento.bytes_enviados,
                "bytes_recibidos": self.rendimiento.bytes_recibidos
            },
            "mac_address": self.rendimiento.mac_address,
            "temperature": self.rendimiento.temperature,
            "date": datetime.now().isoformat()
        }


