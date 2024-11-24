
class Battery:
    def __init__(self, battery_name: str, battery_type: str, voltage: float, resistance: float):
        self.battery_name = battery_name
        self.battery_type = battery_type
        self.voltage = voltage
        self.resistance = resistance
        self.time = 1 # Стандартное значение для всех батарей

    def check_if_damaged(self, calc_current, calc_time):
        self.max_current = self.voltage / self.resistance
        if (calc_current ** 2) * calc_time > (self.max_current ** 2) * self.time:
            return f'Батарея {self.battery_name} повреждена'
        else:
            return f'Батарея {self.battery_name} выдержала'

class Cable:
    def __init__(self, cable_name: str, cable_type: str, section: float, length: float):
        self.cable_name = cable_name
        self.cable_type = cable_type
        self.section = section
        self.length = length
        self.resistivity = 0.017 # Удельное сопротивление меди (Ом*мм2/м)
        self.air_temp = 40 # Температура воздуха
        self.cable_temp = self.air_temp # Температура кабеля до повреждения

    def get_cable_init_resistance(self):
        self.cable_init_resistance = self.resistivity * self.length / self.section
        self.resistance = round(self.cable_init_resistance, 4)
        return self.cable_init_resistance

    def get_cable_changed_resistance(self, dt, i_calc):
        self.cable_temp_new = ((self.cable_temp + 234.5) *
                      (2.71 ** ((dt * (i_calc ** 2))/((226 ** 2) * (self.section ** 2))))
                      - 234.5)
        self.resistance = self.resistance * (1 + 4 * (self.cable_temp_new - self.cable_temp) / 1000)
        self.cable_temp = self.cable_temp_new
        return self.resistance

    def check_if_damaged(self):
        if self.cable_temp_new > 260:
            return (f'Кабель {self.cable_name} нагрелся до температуры {self.cable_temp_new}. '
                    f'Есть риск пожара')
        else:
            return (f'Кабель {self.cable_name} нагрелся до температуры {self.cable_temp_new}. '
                    f'Кабель не поврежден')

class Breaker:
    def __init__(self, breaker_name: str, breaker_type: str, ibreak: float, tbreak: float):
        self.breaker_name = breaker_name
        self.breaker_type = breaker_type
        self.ibreak = ibreak
        self.tbreak = tbreak

class Fuse:
    def __init__(self, fuse_name: str, fuse_type: str, inom: float, tnom: float):
        self.fuse_name = fuse_name
        self.fuse_type = fuse_type
        self.inom = inom
        self.tnom = tnom


def calculation(battery, cable, current_type, fuse=None, breaker=None):
    print('ПОШЛО')
    print(battery)



# if __name__ == '__main__':
    # dt = 0.001  # Время одной итерации
    # t_otkl = 0.2
    # step = t_otkl / dt  # Количество итераций
    # step = int(step)
    # time = 0
    #
    # battery = Battery('Батарея №1','14Groe2000', 230,10)
    # cable = Cable('Кабель №1', 'ВВГ', 10,100)
    # cable_r = cable.get_cable_init_resistance()
    # print(cable_r)
    # i_calc = battery.voltage / (battery.resistance + cable_r)
    # print(f'Начальное значение тока КЗ равно {round(i_calc, 2)} кA')
    #
    # for iter in range(0, step):
    #     time = time + dt
    #     if time <= t_otkl:
    #         i_calc = battery.voltage / (battery.resistance + cable_r)
    #         cable_r = cable.get_cable_changed_resistance(dt, i_calc)
    #         print(cable_r)
    #
    # print(f'Время отключения равно: {time} c')
    # cable.check_if_damaged()