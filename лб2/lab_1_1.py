# 1.1
a = float(input('Задание 1.1 \nВведите первое число: '))
b = float(input('Введите второе число: '))
c = float(input('Введите третье число: '))

min_num = min(a, b, c)

print('Наименьшее число: ', min_num)

# 1.2
print('\nЗадание 1.2')
numbers = []
for i in range(3):
    num = float(input(f"Введите число {i + 1}: "))
    numbers.append(num)

print("Числа в интервале от 1 до 50:")
for num in numbers:
    if 1 <= num <= 50:
        print(num)

# 1.3
m = float(input("\nЗадание 1.3 \nВведите вещественное число m: "))

print("Последовательность:")
for i in range(1, 11):
    result = i * m
    print(f"{i} * {m} = {result}")

# Задание 1.4
print("\nЗадание 1.4")
print("Введите целые числа (для завершения оставьте строку пустой и нажмите Enter):")

numbers = []

# Считываем числа до тех пор, пока не введено ''
while True:
    ch = input("Введите число: ")
    if ch == '':
        break
    try:
        numbers.append(int(ch))
    except ValueError:
        print("Ошибка: введите целое число или оставьте строку пустой для завершения")

if len(numbers) == 0:
    print("Последовательность пуста!")
else:
    sum_numbers = 0
    count = 0
    index = 0

    while index < len(numbers):
        sum_numbers += numbers[index]
        count += 1
        index += 1

    # Выводим результаты
    print(f"Сумма всех чисел: {sum_numbers}")
    print(f"Количество всех чисел: {count}")