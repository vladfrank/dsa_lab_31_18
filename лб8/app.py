import json
import os
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Конфигурация лимитов
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="memory://"
)

# Загрузка и сохранение данных
DATA_FILE = "data.json"

# Загрузка данных из json файла на старте приложения
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Сохранение данных в json после каждой операции
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#хранилище
data_store = load_data()

#сохранить ключ-значение
@app.route("/set", methods=["POST"])
@limiter.limit("10 per minute")   # отдельный лимит
def set_key():
    # ключ значение JSON: {"key": "some_key", "value": "some_value"}
    content = request.get_json()
    if not content or "key" not in content or "value" not in content:
        return jsonify({"error": "Необходимо передать JSON с полями 'key' и 'value'"}), 400
    
    key = content["key"]
    value = content["value"]
    data_store[key] = value
    save_data(data_store)
    return jsonify({"status": "ok", "message": f"Ключ '{key}' сохранён"}), 200

# получить значение по ключу
@app.route("/get/<string:key>", methods=["GET"])
def get_key(key):
    if key in data_store:
        return jsonify({"key": key, "value": data_store[key]}), 200
    else:
        return jsonify({"error": f"Ключ '{key}' не найден"}), 404

# удалить ключ
@app.route("/delete/<string:key>", methods=["DELETE"])
@limiter.limit("10 per minute")   # отдельный лимит
def delete_key(key):
    if key in data_store:
        del data_store[key]
        save_data(data_store)
        return jsonify({"status": "ok", "message": f"Ключ '{key}' удалён"}), 200
    else:
        return jsonify({"error": f"Ключ '{key}' не найден"}), 404

# проверить наличие ключа
@app.route("/exists/<string:key>", methods=["GET"])
def exists_key(key):
    exists = key in data_store
    return jsonify({"key": key, "exists": exists}), 200

# Запуск
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)