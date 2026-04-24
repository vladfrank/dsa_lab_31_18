import pytest
from triangle_class import Triangle, IncorrectTriangleSides

# Позитивные тесты

class TestTrianglePositive:

    def test_equilateral_triangle(self):
        # Создание равностороннего треугольника
        triangle = Triangle(3, 3, 3)
        assert triangle.triangle_type() == "equilateral"
        assert triangle.perimeter() == 9

    def test_equilateral_triangle_float(self):
        # Создание равностороннего треугольника с вещественными числами
        triangle = Triangle(2.5, 2.5, 2.5)
        assert triangle.triangle_type() == "equilateral"
        assert triangle.perimeter() == 7.5

    def test_isosceles_triangle(self):
        # Создание равнобедренного треугольника
        triangle = Triangle(3, 3, 5)
        assert triangle.triangle_type() == "isosceles"
        assert triangle.perimeter() == 11

    def test_isosceles_triangle_different_sides(self):
        # Создание равнобедренного треугольника (разный порядок сторон)
        triangle1 = Triangle(5, 3, 5)
        triangle2 = Triangle(3, 5, 5)
        assert triangle1.triangle_type() == "isosceles"
        assert triangle2.triangle_type() == "isosceles"
        assert triangle1.perimeter() == triangle2.perimeter()

    def test_isosceles_triangle_float(self):
        # Создание равнобедренного треугольника с вещественными числами
        triangle = Triangle(2.5, 2.5, 3)
        assert triangle.triangle_type() == "isosceles"
        assert triangle.perimeter() == 8.0

    def test_nonequilateral_triangle(self):
        # Создание разностороннего треугольника
        triangle = Triangle(3, 4, 5)
        assert triangle.triangle_type() == "nonequilateral"
        assert triangle.perimeter() == 12

    def test_nonequilateral_triangle_float(self):
        # Создание разностороннего треугольника с вещественными числами
        triangle = Triangle(2.2, 3.3, 4.4)
        assert triangle.triangle_type() == "nonequilateral"
        assert triangle.perimeter() == 9.9

    def test_perimeter_big(self):
        # Периметр с большими числами
        triangle = Triangle(100, 150, 200)
        assert triangle.perimeter() == 450

    def test_attributes_stored(self):
        # Проверка сохранения сторон в атрибутах
        triangle = Triangle(3, 4, 5)
        assert triangle.side1 == 3
        assert triangle.side2 == 4
        assert triangle.side3 == 5


# Негативные тесты

class TestTriangleNegative:

    def test_invalid_type_string(self):
        # Попытка создания треугольника со строковым типом данных
        with pytest.raises(IncorrectTriangleSides) as exc_info:
            Triangle("a", 3, 4)
        assert "числами" in str(exc_info.value)

    def test_invalid_type_none(self):
        # Попытка создания треугольника с None
        with pytest.raises(IncorrectTriangleSides):
            Triangle(None, 3, 4)

    def test_zero_side_1(self):
        # Попытка создания с нулевой первой стороной
        with pytest.raises(IncorrectTriangleSides) as exc_info:
            Triangle(0, 3, 4)
        assert "положительными" in str(exc_info.value)

    def test_zero_side_2(self):
        # Попытка создания с нулевой второй стороной
        with pytest.raises(IncorrectTriangleSides):
            Triangle(3, 0, 4)

    def test_zero_side_3(self):
        # Попытка создания с нулевой третьей стороной
        with pytest.raises(IncorrectTriangleSides):
            Triangle(3, 4, 0)

    def test_negative_side_1(self):
        # Попытка создания с отрицательной первой стороной
        with pytest.raises(IncorrectTriangleSides):
            Triangle(-1, 3, 4)

    def test_negative_side_2(self):
        # Попытка создания с отрицательной второй стороной
        with pytest.raises(IncorrectTriangleSides):
            Triangle(3, -2, 4)

    def test_negative_side_3(self):
        # Попытка создания с отрицательной третьей стороной
        with pytest.raises(IncorrectTriangleSides):
            Triangle(3, 4, -1)

    def test_all_negative(self):
        # Попытка создания со всеми отрицательными сторонами
        with pytest.raises(IncorrectTriangleSides):
            Triangle(-1, -1, -1)

    def test_triangle_inequality_3(self):
        # сумма двух сторон меньше третьей
        with pytest.raises(IncorrectTriangleSides) as exc_info:
            Triangle(1, 1, 3)
        assert "не образуют" in str(exc_info.value)

    def test_triangle_inequality_2(self):
        # сумма 1 и 3 сторон меньше второй
        with pytest.raises(IncorrectTriangleSides):
            Triangle(2, 6, 3)

    def test_triangle_inequality_large(self):
        # сумма 2 и 3 сторон меньше первой + большие числа
        with pytest.raises(IncorrectTriangleSides):
            Triangle(10, 1, 1)

    def test_triangle_oneline_1(self):
        # Вырожденный треугольник 1
        with pytest.raises(IncorrectTriangleSides):
            Triangle(1, 2, 3)

    def test_triangle_oneline_2(self):
        # Вырожденный треугольник 2
        with pytest.raises(IncorrectTriangleSides):
            Triangle(5, 10, 5)

    def test_triangle_oneline_3(self):
        # Вырожденный треугольник 3
        with pytest.raises(IncorrectTriangleSides):
            Triangle(5, 3, 2)