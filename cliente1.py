import requests 
#La biblioteca requests es una librería popular en Python para hacer peticiones HTTP

url = 'http://localhost:5000/log'
headers = {
    'Content-Type': 'application/json',
    'Authorization': '123'
}

log_data = {
    'timestamp': '2024-08-06 14:00:00',
    'service_name': 'cliente-1',
    'severity': 'debug',
    'message': 'Valor de la variable X durante la ejecución: 42'
}

response = requests.post(url, json=log_data, headers=headers)
print(response.json())
