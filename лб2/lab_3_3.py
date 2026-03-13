#3.3
import sys

# Получаем аргументы командной строки
args = sys.argv[1:]

# Создаем пустой массив
array = []

# Заполняем массив числами из командной строки
i = 0
while i < len(args):
    # Преобразуем текст в число и добавляем в массив
    array.append(int(args[i]))
    i += 1

# Находим сумму элементов с нечетными индексами
n = len(array)
summa = 0
i = 0
while i < n:
    if i % 2 == 1:  # если индекс нечетный
        summa = summa + array[i]
    i += 1

# Выводим сумму
print(summa)

# Заменяем элементы меньше 15 на удвоенные
i = 0
while i < n:
    if array[i] < 15:
        array[i] = array[i] * 2
    i += 1

# Выводим измененный массив
print(array)