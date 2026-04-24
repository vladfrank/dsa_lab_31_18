# исключение при некорректных сторонах треугольника
class IncorrectTriangleSides(Exception):
    pass


class Triangle:
    def __init__(self, side1, side2, side3):
        # Проверка типов данных
        if not isinstance(side1, (int, float)) or \
                not isinstance(side2, (int, float)) or \
                not isinstance(side3, (int, float)):
            raise IncorrectTriangleSides("Все стороны должны быть числами")

        # 1. все стороны должны быть положительными
        if side1 <= 0 or side2 <= 0 or side3 <= 0:
            raise IncorrectTriangleSides("Длины сторон должны быть положительными числами")

        # 2. правило неравенства треугольника
        if (side1 + side2 <= side3) or (side1 + side3 <= side2) or (side2 + side3 <= side1):
            raise IncorrectTriangleSides("Стороны не образуют треугольник")

        # Сохраняем стороны
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

# определяет тип треугольника
    def triangle_type(self):
        if self.side1 == self.side2 == self.side3:
            return "equilateral"
        elif self.side1 == self.side2 or self.side1 == self.side3 or self.side2 == self.side3:
            return "isosceles"
        else:
            return "nonequilateral"

# вычисляет периметр треугольника
    def perimeter(self):
        return self.side1 + self.side2 + self.side3