class Battery:
    """
    Класс, описывающий элемент аккумуляторная батарея.
    """

    def __init__(self,
                 battery_name: str,
                 battery_type: str,
                 voltage: float,
                 resistance: float):
        self.battery_name = battery_name
        self.battery_type = battery_type
        self.voltage = voltage
        self.resistance = resistance
        self.time = 1  # Стандартное значение для всех батарей

    def check_if_damaged(self, calc_current: float, calc_time: float) -> str:
        """
        Проверяет состояние батареи в конце расчета.
        Args:
            calc_current: Рассчитанный ток.
            calc_time: Длительность аварии.

        Returns:
            Строка с информацией - поврежден ли элемент.
        """
        self.max_current = self.voltage / self.resistance
        if ((calc_current ** 2) * calc_time >
                ((self.max_current * 1000) ** 2) * self.time):
            return f'Батарея {self.battery_name} повреждена.'
        else:
            return f'Батарея {self.battery_name} выдержала.'


class Cable:
    """
    Класс, описывающий элемент аккумуляторная батарея.
    """

    def __init__(self,
                 cable_name: str,
                 cable_type: str,
                 section: float,
                 length: float):
        self.cable_name = cable_name
        self.cable_type = cable_type
        self.section = section
        self.length = length
        # Удельное сопротивление меди (Ом*мм2/м):
        self.resistivity = 0.017
        # Температура воздуха:
        self.air_temp = 40
        # Температура кабеля до повреждения:
        self.cable_temp = self.air_temp

    def get_cable_init_resistance(self) -> float:
        """
        Рассчитывает исходное сопротивление кабеля.

        Returns:
            Возвращает рассчитанное значение сопротивления.

        """
        self.cable_init_resistance = (
                1000 * self.resistivity * self.length / self.section)
        self.resistance = round(self.cable_init_resistance, 0)
        return self.cable_init_resistance

    def get_cable_changed_resistance(self, dt: float, i_calc: float):
        """
        Рассчитывает измененное сопротивление кабеля.

        Returns:
            Возвращает рассчитанное значение сопротивления.

        """

        self.cable_temp_new = \
            ((self.cable_temp + 234.5) *
             (2.71 ** ((dt * (i_calc ** 2)) /
                       ((226 ** 2) * (self.section ** 2)))) - 234.5)
        self.resistance = (self.resistance *
                           (1 + 4 * (self.cable_temp_new - self.cable_temp)
                            / 1000))
        self.cable_temp = self.cable_temp_new
        return self.resistance

    def check_if_damaged(self):
        """
        Проверяет повреждение элемента.

        Returns:
            Строка с информацией - поврежден ли элемент.

        """
        if self.cable_temp_new > 260:
            return (f'Кабель {self.cable_name} нагрелся '
                    f'до температуры {round(self.cable_temp_new, 0)}°С. '
                    f'Есть риск пожара.')
        else:
            return (f'Кабель {self.cable_name} нагрелся '
                    f'до температуры {round(self.cable_temp_new, 0)}°С. '
                    f'Кабель не поврежден.')


class Breaker:
    """
    Класс, описывающий элемент выключатель.

    """

    def __init__(self,
                 breaker_name: str,
                 breaker_type: str,
                 ibreak: float,
                 tbreak: float):
        self.breaker_name = breaker_name
        self.breaker_type = breaker_type
        self.ibreak = ibreak
        self.tbreak = tbreak

    def check_if_damaged(self, i_calc):
        """
        Проверяет поврежден ли элемент
        Args:
            i_calc: Рассчитанный ток в цепи.

        Returns:
            Строка с информацией - поврежден ли элемент.

        """

        self.ibreak_max = self.ibreak * 100
        if self.ibreak_max > i_calc:
            return (f'Ток не превысил отключающую '
                    f'способность выключателя {self.breaker_name}, '
                    f'равную {round(self.ibreak_max, 0)} А. '
                    f'Выключатель не повредился.')
        else:
            return (f'Ток превысил отключающую '
                    f'способность выключателя {self.breaker_name}, '
                    f'равную {round(self.ibreak_max, 0)} А. '
                    f'Выключатель повредился.')


class Fuse:
    """
    Класс, описывающий элемент предохранитель.

    """

    def __init__(self,
                 fuse_name: str,
                 fuse_type: str,
                 inom: float,
                 tnom: float):
        self.fuse_name = fuse_name
        self.fuse_type = fuse_type
        self.inom = inom
        self.tnom = tnom  # время за которое отключит ток 5 крат


def calculation(battery,
                cable,
                current_type,
                fuse=None,
                breaker=None) -> list:
    """
        Рассчитывает ток цепи и ряд дополнительных параметров.
    Args:
        battery: Объект класса Battery.
        cable: Объект класса Cable.
        current_type:
        fuse: Объект класса Fuse.
        breaker: Объект класса Breaker.

    Returns:
        Список, элементы которого содержат информацию о результатах расчета.
    """
    dt = 0.001  # время (секунды) одной итерации
    if breaker is not None:
        tbreak = breaker.tbreak  # время (секунды) одной итерации
    time = 0  # время начала повреждения
    u = battery.voltage
    r1 = battery.resistance
    r2 = cable.get_cable_init_resistance()
    if current_type == 'Дуговое замыкание':
        r3 = 5
    else:
        r3 = 0
    # Начальное значение тока:
    i_first = 1000 * u / (r1 + r2 + r3)
    i_calc = i_first

    if breaker is not None:
        while time < tbreak:
            r2 = cable.get_cable_changed_resistance(dt, i_calc)
            i_calc = 1000 * u / (r1 + r2 + r3)
            time += dt
        time = 100 * time / 100
        check_bat = battery.check_if_damaged(i_calc, time)
        check_cab = cable.check_if_damaged()
        check_breaker = breaker.check_if_damaged(i_calc)

        return [f'Вид повреждения: {current_type}',
                f'Начальное значение тока: {round(i_first, 0)} А.',
                f'Значение тока к моменту отключения: {round(i_calc, 0)} А.',
                f'Время отключения тока: {round(time, 0)} c.',
                check_bat, check_cab, check_breaker
                ]
    elif fuse is not None:
        while True:
            r2 = cable.get_cable_changed_resistance(dt, i_calc)
            i_calc = 1000 * u / (r1 + r2 + r3)
            tfuse = fuse.tnom
            if tfuse > time:
                time += dt
            elif tfuse <= time <= 10:
                check_fuse = 'Предохранитель отключил ток'
                time = 100 * tfuse / 100
                check_bat = battery.check_if_damaged(i_calc, time)
                check_cab = cable.check_if_damaged()
                break
            else:
                check_fuse = 'Предохранитель не отключил ток'
                break

        if check_fuse == 'Предохранитель отключил ток':
            return [f'Вид повреждения: {current_type}',
                    f'Начальное значение тока: '
                    f'{round(i_first, 0)} А.',
                    f'Значение тока к моменту отключения: '
                    f'{round(i_calc, 0)} А.',
                    f'Время отключения тока: {round(time, 2)} c.',
                    check_bat, check_cab]

        elif check_fuse == 'Предохранитель не отключил ток':
            return [f'Вид повреждения: {current_type}',
                    f'Начальное значение тока: {round(i_first, 0)} А.',
                    'Предохранитель не отключил ток. Необходимо выбрать '
                    'другой предохранитель, '
                    'или увеличить сечение кабеля, или изменить схему.']


if __name__ == '__main__':
    battery = Battery('Батарея 1', 'Тип 1', 225, 5)
    cable = Cable('Кабель 1', 'Тип 2', 60, 100)
    breaker = Breaker('Выключатель 1', 'Тип 3', 100, 5)
    fuse = Fuse('Предохранитель 1', 'PNA100', 500, 5)

    x = calculation(battery, cable, 'Металлическое замыкание', breaker=breaker)
    for val in x:
        print(val)

    print()

    y = calculation(battery, cable, 'Дуговое замыкание', fuse=fuse)
    for val in y:
        print(val)
