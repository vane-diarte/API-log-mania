import requests

url = 'http://localhost:5000/log'
headers = {
    'Content-Type': 'application/json',
    'Authorization': '789'  
}

log_data = {
    'timestamp': '2024-08-08 12:00:00',
    'service_name': 'cliente-3',
    'severity': 'info',
    'message': 'El sistema se ha iniciado correctamente'
}

response = requests.post(url, json=log_data, headers=headers)
print(response.json())