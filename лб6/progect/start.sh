#!/bin/bash


python currency-manager.py &
python data-manager.py &
cd gateway
python app.py &
echo "Все микросервисы запущены"
echo "Ссылка: http://localhost:5000"
wait