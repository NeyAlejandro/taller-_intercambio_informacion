import psutil
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Direcciones de correo electrónico
correo_emisor = 'charroney497@gmail.com'
correo_destinatario = 'juanman042023@gmail.com'
clave_correo_emisor = '1002079000'

def enviar_correo(asunto, cuerpo):
    mensaje = MIMEMultipart()
    mensaje['From'] = correo_emisor
    mensaje['To'] = correo_destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(correo_emisor, clave_correo_emisor)
        texto = mensaje.as_string()
        server.sendmail(correo_emisor, correo_destinatario, texto)

def monitorear_cpu():
    while True:
        # Obtener el porcentaje de uso del CPU
        uso_cpu = psutil.cpu_percent(interval=1)

        # Imprimir el porcentaje de uso del CPU
        print(f"Uso del CPU: {uso_cpu}%")

        # Verificar si el uso del CPU supera el 40%
        if uso_cpu > 40:
            # Enviar una notificación por correo
            asunto = 'Alerta de Uso Alto del CPU'
            cuerpo = f"¡Alerta! El uso del CPU ha superado el 40%. Actualmente es {uso_cpu}%."
            enviar_correo(asunto, cuerpo)

        # Esperar un breve periodo antes de la siguiente lectura
        time.sleep(1)

if __name__ == "__main__":
    monitorear_cpu()
