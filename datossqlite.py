import sqlite3

def consultar_datos():
    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect('datos_rendimiento.db')

    # Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()

    try:
        # Ejecutar una consulta SQL para seleccionar todos los datos de la tabla datos_rendimiento
        cursor.execute('SELECT * FROM datos_rendimiento')

        # Obtener todos los resultados de la consulta
        resultados = cursor.fetchall()

        # Imprimir los resultados
        for resultado in resultados:
            print(resultado)

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")

    finally:
        # Cerrar la conexión a la base de datos
        conexion.close()

if __name__ == "__main__":
    consultar_datos()