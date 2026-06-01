import requests

BASE_URL = "http://127.0.0.1:5000"

# Сохранить ключ-значение
response = requests.post(f"{BASE_URL}/set", json={"key": "student", "value": "Vlad"})
print("SET:", response.json())

# Получить значение по ключу
response = requests.get(f"{BASE_URL}/get/student")
print("GET:", response.json())

# Проверить существование ключа
response = requests.get(f"{BASE_URL}/exists/student")
print("EXISTS:", response.json())

#  Удалить ключ
response = requests.delete(f"{BASE_URL}/delete/student")
print("DELETE:", response.json())

# Попробовать получить удалённый ключ
response = requests.get(f"{BASE_URL}/get/student")
print("GET after delete:", response.json())
