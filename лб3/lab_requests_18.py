from flask import Flask, request, jsonify
import requests
import random
import threading
import time
import subprocess
import json

app = Flask(__name__)

# GET эндпоинт
@app.route('/number/', methods=['GET'])
def get_number():
    param = request.args.get('param')
    
    if param is None:
        return jsonify({'error': 'Missing parameter "param"'}), 400
    
    try:
        param_num = float(param)
    except ValueError:
        return jsonify({'error': 'Need to send a number'}), 400
    
    result = random.uniform(1, 10) * param_num
    return jsonify({'result': result})

# POST эндпоинт
@app.route('/number/', methods=['POST'])
def post_number():
    data = request.get_json()
    
    if data is None or 'jsonParam' not in data:
        return jsonify({'error': 'Missing value "jsonParam"'}), 400
    
    try:
        param_num = float(data['jsonParam'])
    except (ValueError, TypeError):
        return jsonify({'error': 'jsonParam must be a number'}), 400
    
    result = random.uniform(1, 100) * param_num
    operation = random.choice(['sum', 'sub', 'mul', 'div'])
    
    return jsonify({'result': result, 'operation': operation})

# DELETE эндпоинт
@app.route('/number/', methods=['DELETE'])
def delete_number():
    return jsonify({
        'number': random.uniform(1, 100),
        'operation': random.choice(['sum', 'sub', 'mul', 'div'])
    })

def run_server():
    app.run(debug=False, port=5000, use_reloader=False)

def apply_operation(value, operation, value2):
    if operation == 'sum':
        return value + value2
    elif operation == 'sub':
        return value - value2
    elif operation == 'mul':
        return value * value2
    elif operation == 'div' and value2 != 0:
        return value / value2
    return value

def send_requests():
    time.sleep(2)
    url = "http://localhost:5000/number/"
    
    print("\nЗапросы requests")
    
    # GET запрос
    param = random.randint(1, 10)
    print(f"GET /number/?param={param}")
    response = requests.get(url, params={"param": param}).json()
    result = response['result']
    print(f"Ответ: {{'result': {result}}}\n")
    
    # POST запрос
    json_param = random.randint(1, 10)
    print(f"POST /number/")
    print(f"Body: {{'jsonParam': {json_param}}}")
    response = requests.post(url, json={"jsonParam": json_param}).json()
    post_result = response['result']
    post_op = response['operation']
    print(f"Ответ: {{'result': {post_result}, 'operation': '{post_op}'}}\n")
    
    # DELETE запрос
    print("DELETE /number/")
    response = requests.delete(url).json()
    del_num = response['number']
    del_op = response['operation']
    print(f"Ответ: {{'number': {del_num}, 'operation': '{del_op}'}}\n")
    
    # Вычисления
    print(f"Начальное значение: {result}")
    print(f"Шаг 1: {result} {post_op} {post_result} = ", end="")
    result = apply_operation(result, post_op, post_result)
    print(result)
    
    print(f"Шаг 2: {result} {del_op} {del_num} = ", end="")
    result = apply_operation(result, del_op, del_num)
    print(result)
    
    print(f"\nРЕЗУЛЬТАТ (int): {int(result)}")

def send_requests_curl():
    url = "http://localhost:5000/number/"
    
    print("\n Запросы curl")
    
    # GET запрос
    param = random.randint(1, 10)
    print(f"curl -X GET '{url}?param={param}'")
    # -s вывд без прогресса и ошибок
    # capture_output=True - берем результат из консоли
    curl_result = subprocess.run(['curl', '-s', f'{url}?param={param}'], 
                                  capture_output=True, text=True)
    data = json.loads(curl_result.stdout)
    result = data['result']
    print(f"Ответ: {{'result': {result}}}\n")
    
    # POST запрос
    json_param = random.randint(1, 10)
    json_body = f'{{"jsonParam": {json_param}}}'
    print(f"curl -X POST {url} -H 'Content-Type: application/json' -d '{json_body}'")
    # -X - тип запроса
    # -H - заголовок
    # -d - тело запроса
    curl_result = subprocess.run(['curl', '-s', '-X', 'POST', url, 
                                  '-H', 'Content-Type: application/json', 
                                  '-d', json_body], capture_output=True, text=True)
    data = json.loads(curl_result.stdout)
    post_result = data['result']
    post_op = data['operation']
    print(f"Ответ: {{'result': {post_result}, 'operation': '{post_op}'}}\n")
    
    # DELETE запрос
    print(f"curl -X DELETE {url}")
    curl_result = subprocess.run(['curl', '-s', '-X', 'DELETE', url], 
                                  capture_output=True, text=True)
    data = json.loads(curl_result.stdout)
    del_num = data['number']
    del_op = data['operation']
    print(f"Ответ: {{'number': {del_num}, 'operation': '{del_op}'}}\n")
    
    # Вычисления
    print(f"Начальное значение: {result}")
    print(f"Шаг 1: {result} {post_op} {post_result} = ", end="")
    result = apply_operation(result, post_op, post_result)
    print(result)
    
    print(f"Шаг 2: {result} {del_op} {del_num} = ", end="")
    result = apply_operation(result, del_op, del_num)
    print(result)
    
    print(f"\nРЕЗУЛЬТАТ (int): {int(result)}")

if __name__ == '__main__':
    #поток для парралельного запуска сервера в фоновом режиме, который выключится после выполнений запросов через функции
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    send_requests()
    send_requests_curl()