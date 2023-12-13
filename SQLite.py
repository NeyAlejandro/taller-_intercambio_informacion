import sqlite3

class BaseDatosSQLite:
    def __init__(self, filename):
        self.filename = filename
        self._conexion_db = sqlite3.connect(filename)
        self._crear_tabla()

    def _crear_tabla(self):
        cursor = self._conexion_db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_rendimiento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_percent REAL,
                memory_percent REAL,
                bytes_enviados INTEGER,
                bytes_recibidos INTEGER,
                mac_address TEXT,
                temperature REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self._conexion_db.commit()

    def insertar_datos(self, datos_rendimiento):
        cursor = self._conexion_db.cursor()
        cursor.execute('''
            INSERT INTO datos_rendimiento (
                cpu_percent,
                memory_percent,
                bytes_enviados,
                bytes_recibidos,
                mac_address,
                temperature
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (datos_rendimiento.rendimiento.cpu_percent, datos_rendimiento.rendimiento.memory_percent,
              datos_rendimiento.rendimiento.bytes_enviados, datos_rendimiento.rendimiento.bytes_recibidos,
              datos_rendimiento.rendimiento.mac_address, datos_rendimiento.rendimiento.temperature))
        self._conexion_db.commit()

    def cerrar_conexion(self):
        self._conexion_db.close()


if __name__ == "__main__":
    obtener_datos_y_guardar()
    consultar_datos()
