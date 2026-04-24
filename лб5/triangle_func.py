# исключение при некорректных сторонах треугольника
class IncorrectTriangleSides(Exception):
    pass


def get_triangle_type(side1, side2, side3):
    # Проверка типов данных
    if not isinstance(side1, (int, float)) or \
       not isinstance(side2, (int, float)) or \
       not isinstance(side3, (int, float)):
        raise IncorrectTriangleSides("Все стороны должны быть числами")

    # 1. все стороны должны быть положительными числами
    if side1 <= 0 or side2 <= 0 or side3 <= 0:
        raise IncorrectTriangleSides("Длины сторон должны быть положительными числами")

    # 2. сумма любых двух сторон должна быть больше третьей (правило неравенства треугольника)
    if (side1 + side2 <= side3) or (side1 + side3 <= side2) or (side2 + side3 <= side1):
        raise IncorrectTriangleSides("Стороны не образуют треугольник")

    # Определение типа треугольника
    if side1 == side2 == side3:
        # равносторонний
        return "equilateral"
    elif side1 == side2 or side1 == side3 or side2 == side3:
        # ровнобедренный
        return "isosceles"
    else:
        # разносторонний
        return "nonequilateral"