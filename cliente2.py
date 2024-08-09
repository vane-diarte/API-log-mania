import requests

url = 'http://localhost:5000/log'
headers = {
    'Content-Type': 'application/json',
    'Authorization': '456'
}

log_data = {
    'timestamp': '2024-08-07 13:00:00',
    'service_name': 'cliente-2',
    'severity': 'error',
    'message': 'Error al conectar con la base de datos'
}

response = requests.post(url, json=log_data, headers=headers)
print(response.json())