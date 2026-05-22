import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Адреса микросервисов
CURRENCY_MANAGER_URL = "http://localhost:5001"
DATA_MANAGER_URL = "http://localhost:5002"


# Главная страница
@app.route("/")
def index():
    return render_template("index.html")


# Прокси для POST /load (currency-manager)
@app.route("/load", methods=["POST"])
def proxy_load():
    # Читаем данные из HTML-формы
    currency_name = request.form.get("currency_name")
    rate = request.form.get("rate")
    
    # Проверяем, что оба поля заполнены
    if not currency_name or not rate:
        return render_template("index.html", error="Missing currency_name or rate")
    
    # Отправляем POST-запрос к микросервису currency-manager (эндпоинт /load)
    resp = requests.post(f"{CURRENCY_MANAGER_URL}/load", json={
        "currency_name": currency_name,
        "rate": float(rate)
    })
    
    # Если ответ от микросервиса 200 OK показываем сообщение об успехе
    if resp.status_code == 200:
        return render_template("index.html", message=f"Валюта {currency_name} добавлена")
    else:
        # Иначе текст ошибки 
        error_msg = resp.json().get("error", "Unknown error")
        return render_template("index.html", error=error_msg)


# Прокси для POST /update_currency (currency-manager)
@app.route("/update", methods=["POST"])
def proxy_update():
    # Читаем данные из HTML-формы
    currency_name = request.form.get("currency_name")
    rate = request.form.get("rate")
    
    # Проверяем, что оба поля заполнены
    if not currency_name or not rate:
        return render_template("index.html", error="Missing currency_name or rate")
    
    # Отправляем POST запрос
    resp = requests.post(f"{CURRENCY_MANAGER_URL}/update_currency", json={
        "currency_name": currency_name,
        "rate": float(rate)
    })
    
    #если получили ответ 200 сообщение об успехе иначе текст ошибки
    if resp.status_code == 200:
        return render_template("index.html", message=f"Курс {currency_name} обновлён")
    else:
        error_msg = resp.json().get("error", "Unknown error")
        return render_template("index.html", error=error_msg)


# Прокси для POST /delete (currency-manager)
@app.route("/delete", methods=["POST"])
def proxy_delete():
    currency_name = request.form.get("currency_name")
    
    if not currency_name:
        return render_template("index.html", error="Missing currency_name")
    
    resp = requests.post(f"{CURRENCY_MANAGER_URL}/delete", json={
        "currency_name": currency_name
    })
    
    if resp.status_code == 200:
        return render_template("index.html", message=f"Валюта {currency_name} удалена")
    else:
        error_msg = resp.json().get("error", "Unknown error")
        return render_template("index.html", error=error_msg)


# Прокси для GET /convert (data-manager)
@app.route("/convert", methods=["GET"])
def proxy_convert():
    # Читаем параметры из строки запроса
    currency_name = request.args.get("currency_name")
    amount = request.args.get("amount")
    
    if not currency_name or not amount:
        return render_template("index.html", error="Missing currency_name or amount")
    
    # GET-запрос к data-manager, параметры передаём через params=
    resp = requests.get(f"{DATA_MANAGER_URL}/convert", params={
        "currency_name": currency_name,
        "amount": amount
    })
    
    if resp.status_code == 200:
        # Из ответа извлекаем сконвертированную сумму
        converted = resp.json().get("converted")
        return render_template("index.html", message=f"{amount} {currency_name} = {converted} RUB")
    else:
        error_msg = resp.json().get("error", "Unknown error")
        return render_template("index.html", error=error_msg)


# Прокси для GET /currencies (data-manager)
@app.route("/currencies", methods=["GET"])
def proxy_currencies():
    # Отправляем запрос к data-manager
    resp = requests.get(f"{DATA_MANAGER_URL}/currencies")
    
    if resp.status_code == 200:
        # Получаем список валют (список словарей) и передаём в шаблон
        currencies = resp.json()
        return render_template("index.html", currencies=currencies)
    else:
        return render_template("index.html", error="Failed to fetch currencies")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)