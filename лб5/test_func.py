import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides


class TestGetTriangleType(unittest.TestCase):


    # Позитивное тестирование
    def test_equilateral_triangle(self):
        # Равносторонний (equilateral) треугольник
        self.assertEqual(get_triangle_type(3, 3, 3), "equilateral")
        self.assertEqual(get_triangle_type(5, 5, 5), "equilateral")
        self.assertEqual(get_triangle_type(0.5, 0.5, 0.5), "equilateral")

    def test_isosceles_triangle(self):
        # Равнобедренный (isosceles) треугольник
        self.assertEqual(get_triangle_type(3, 3, 5), "isosceles")
        self.assertEqual(get_triangle_type(5, 3, 5), "isosceles")
        self.assertEqual(get_triangle_type(3, 5, 5), "isosceles")
        self.assertEqual(get_triangle_type(2, 2, 3.5), "isosceles")
        self.assertEqual(get_triangle_type(2.5, 2.5, 3), "isosceles")

    def test_nonequilateral_triangle(self):
        # Разносторонний (nonequilateral) треугольник
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")
        self.assertEqual(get_triangle_type(5, 6, 7), "nonequilateral")
        self.assertEqual(get_triangle_type(2.2, 3.3, 4.4), "nonequilateral")


    # Негативное тестирование (должно вызвать IncorrectTriangleSides)
    def test_invalid_data_types(self):
        # Некорректные типы данных
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type("a", 3, 4)  # строковое значение
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(None, 3, 4)  # None значение

    def test_zero_sides(self):
        # Нулевые стороны
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 3, 4)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(3, 0, 4)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(3, 4, 0)

    def test_negative_sides(self):
        # Отрицательные стороны
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 3, 4)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(3, -2, 4)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(3, 4, -1)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, -1, -1)

    def test_triangle_inequality(self):
        # Нарушение неравенства треугольника (сумма двух сторон меньше третьей)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 1, 3)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(2, 6, 3)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(10, 1, 1)

    def test_oneline_triangle(self):
        # Вырожденный треугольник (точки на одной прямой)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 3)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(5, 10, 5)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(5, 3, 2)


if __name__ == "__main__":
    unittest.main()