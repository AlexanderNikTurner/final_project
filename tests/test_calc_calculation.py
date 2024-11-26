import unittest

from calc_calculation import calculation, Battery, Cable, Breaker, Fuse


class TestCalculation(unittest.TestCase):

    def setUp(self):
        self.battery = Battery('Батарея 1', 'Тип 1', 225, 5)
        self.cable = Cable('Кабель 1', 'Тип 2', 60, 100)
        self.breaker = Breaker('Выключатель 1', 'Тип 3', 100, 5)
        self.fuse = Fuse('Предохранитель 1', 'PNA100', 500, 5)

    def test_type_of_failure(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[0],
                         'Вид повреждения: Металлическое замыкание',
                         'Неверно выводит вид повреждения')

    def test_result_value(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[1],
                         'Начальное значение тока: 6750.0 А.',
                         'Ошибка в расчете начального значения.')

    def test_result_final_value(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[2],
                         'Значение тока к моменту отключения: 3167.0 А.',
                         'Ошибка в расчете итогового значения.')

    def test_result_time(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[3],
                         'Время отключения тока: 5.0 c.',
                         'Неверно считает время отключения.')

    def test_result_battery_damage(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[4],
                         'Батарея Батарея 1 выдержала.',
                         'Неверно работает метод определения '
                         'повреждения батареи.')

    def test_result_cable_damage(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[5],
                         'Кабель Кабель 1 нагрелся до температуры '
                         '255.0°С. Кабель не поврежден.',
                         'Неверно работает метод определения '
                         'повреждения кабеля.')

    def test_result_breaker_damage(self):
        check_result = calculation(self.battery,
                                   self.cable,
                                   'Металлическое замыкание',
                                   breaker=self.breaker)
        self.assertEqual(check_result[6],
                         'Ток не превысил отключающую способность '
                         'выключателя Выключатель 1, равную 10000 А. '
                         'Выключатель не повредился.',
                         'Неверно определяет состояние выключателя.')


if __name__ == '__main__':
    unittest.main()
