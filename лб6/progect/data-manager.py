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


# ЭНДПОИНТ GET /convert
@app.route("/convert", methods=["GET"])
def convert():
    # Берём параметры из адресной строки
    currency_name = request.args.get("currency_name")
    amount_str = request.args.get("amount")

    # Проверка, оба параметра переданы?
    if not currency_name or not amount_str:
        return jsonify({"error": "Missing currency_name or amount"}), 400

    # Преобразуем сумму в число
    try:
        amount = float(amount_str)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400

    currency_name = currency_name.upper()

    with get_db() as conn:
        with conn.cursor() as cur:
            # Ищем курс валюты в БД
            cur.execute("SELECT rate FROM currencies WHERE currency_name = %s", (currency_name,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": f"Currency '{currency_name}' not found"}), 404

            rate = float(row[0])
            converted = amount * rate
            # Возвращаем результат
            return jsonify({"converted": converted}), 200

# ЭНДПОИНТ GET /currencies
# Возвращает все добавленные валюты в виде JSON списка
@app.route("/currencies", methods=["GET"])
def get_currencies():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, currency_name, rate FROM currencies ORDER BY id")
            rows = cur.fetchall()
            # Собираем список валют
            currencies = []
            for row in rows:
                currencies.append({
                    "id": row[0],                
                    "currency_name": row[1],     
                    "rate": float(row[2])         
                })
            return jsonify(currencies), 200

# запуск микросервиса на порту 5002
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)