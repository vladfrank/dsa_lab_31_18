import os
import psycopg2                 
from flask import Flask, request, jsonify

app = Flask(__name__)

# Конфигурация подключения к базе данных 
DB_CONFIG = {
    "host": "localhost",      
    "port": "5432",            
    "database": "rpp",          
    "user": "postgres",         
    "password": "postgres"      
}

def get_db():
    return psycopg2.connect(**DB_CONFIG)

def next_id(cur):
    # Вычисляем следующий доступный id для новой записи.
    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM currencies")
    return cur.fetchone()[0]

# ЭНДПОИНТ POST /load

@app.route("/load", methods=["POST"])
def load():
    # Получаем данные
    data = request.get_json()
    name = data["currency_name"].upper()
    rate = data["rate"]

    # Устанавливаем соединение с БД 
    with get_db() as conn:
        with conn.cursor() as cur:
            # 1. существует ли уже такая валюта в таблице
            cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
            if cur.fetchone():
                # Если существует возвращаем ошибку 409
                return jsonify({"error": "Currency exists"}), 409

            # 2. генерируем новый id и вставляем запись
            cur.execute(
                "INSERT INTO currencies (id, currency_name, rate) VALUES (%s, %s, %s)",
                (next_id(cur), name, rate)
            )
            conn.commit()  

            # 3. возвращаем ответ 200 OK 
            return jsonify({"message": "OK"}), 200


# ЭНДПОИНТ POST /update_currency
@app.route("/update_currency", methods=["POST"])
def update():
    # Получаем данные
    data = request.get_json()
    name = data["currency_name"].upper()
    new_rate = data["rate"]

    with get_db() as conn:
        with conn.cursor() as cur:
            # 1. существует ли уже такая валюта в таблице
            cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
            if not cur.fetchone():
                # если нет вернуть 404 
                return jsonify({"error": "Currency not found"}), 404

            # 2. обновляем курс
            cur.execute("UPDATE currencies SET rate = %s WHERE currency_name = %s", (new_rate, name))
            conn.commit()

            # 3. возвращаем ответ 200 OK
            return jsonify({"message": "OK"}), 200

# ЭНДПОИНТ POST /delete
@app.route("/delete", methods=["POST"])
def delete():
    # Получаем данные
    data = request.get_json()
    name = data["currency_name"].upper()

    with get_db() as conn:
        with conn.cursor() as cur:
            # 1. существует ли уже такая валюта в таблице
            cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
            if not cur.fetchone():
                return jsonify({"error": "Currency not found"}), 404

            # 2. удаляем запись
            cur.execute("DELETE FROM currencies WHERE currency_name = %s", (name,))
            conn.commit()

            # 3. возвращаем ответ 200 OK
            return jsonify({"message": "OK"}), 200

# запуск микросервиса на порту 5001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)