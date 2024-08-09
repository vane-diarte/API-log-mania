from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Lista de API keys válidas
VALID_API_KEYS = ["123", "456", "789", "1011"]

def iniciar_db():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            received_at TEXT,
            service_name TEXT,
            severity TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()


def guardar_log (timestamp, service_name, severity, message):
    received_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, received_at, service_name, severity, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, received_at, service_name, severity, message))
    conn.commit()
    conn.close()


@app.route('/log', methods=['POST']) #recibe un log y lo guarda en la base de datos.
def log():
    api_key = request.headers.get('Authorization')  # Obtiene la API key del encabezado
    if api_key not in VALID_API_KEYS:  # Verifica si la API key es válida
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json #diccionario con los datos json que envia el cliente
    timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
    service_name = data['service_name'] #acceder directamente al valor del diccionario
    severity = data['severity']
    message = data['message']

    guardar_log(timestamp, service_name, severity, message)
    return jsonify({"status": "success"}), 201


@app.route('/obtener_logs', methods=['GET'])
def obtener_logs():
    start_date = request.args.get('start_date') #obtiene los parametros de la url y asigna su valor a la variable
    end_date = request.args.get('end_date')
    start_received_at = request.args.get('start_received_at')
    end_received_at = request.args.get('end_received_at')

    consulta = "SELECT * FROM logs WHERE 1=1"  # Base de la consulta SQL
    parametros = []

    # Añadir condiciones a la consulta según los filtros
    if start_date:
        consulta += " AND timestamp >= ?"
        parametros.append(start_date) #se guarda el valor en la lista parametros si se cumple la condicion
    if end_date:
        consulta += " AND timestamp <= ?"
        parametros.append(end_date)
    if start_received_at:
        consulta += " AND received_at >= ?"
        parametros.append(start_received_at)
    if end_received_at:
        consulta += " AND received_at <= ?"
        parametros.append(end_received_at)

    # Ejecutar la consulta y obtener los resultados
    conn = sqlite3.connect('logs.db') #establece la conexion con la base de datos
    cursor = conn.cursor()
    cursor.execute(consulta, parametros)
    logs = cursor.fetchall() #devuelve una lista de tuplas con todos los resultados de la consulta
    conn.close()

    # Convertir los resultados en una lista de diccionarios
    lista_de_logs = []
    for log in logs:
        lista_de_logs.append({
            "id": log[0], #accede a los valores especificos de la tupla y los agrega como valor a las claves del diccionario
            "timestamp": log[1],
            "received_at": log[2],
            "service_name": log[3],
            "severity": log[4],
            "message": log[5]
        })

    return jsonify(lista_de_logs), 200

if __name__ == '__main__':
    iniciar_db()  # Inicializar la base de datos al iniciar la aplicación
    app.run(port=5000)  # Ejecutar la aplicación en el puerto 5000
