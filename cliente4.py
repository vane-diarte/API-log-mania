import requests

url = 'http://localhost:5000/log'
headers = {
    'Content-Type': 'application/json',
    'Authorization': '1011'
}

log_data = {
    'timestamp': '2024-08-09 17:00:00',
    'service_name': 'cliente-4', 
    'severity': 'warning',
    'message': 'Memoria disponible baja, considere liberar recursos'
}

response = requests.post(url, json=log_data, headers=headers)
print(response.json())  # Imprimir la respuesta del servidor
