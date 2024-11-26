import sqlite3


class BatteriesDataBase:
    """
    Класс для работы с базой аккумуляторных батарей.

    """

    @staticmethod
    def add(battery_type: str, voltage: float, resistance: float):
        """
        Добавляет батарею в базу.
        Args:
            battery_type: Тип аккумуляторной батареи.
            voltage: Напряжение аккумуляторной батареи.
            resistance: Сопротивление аккумуляторной батареи.

        """
        connection = sqlite3.connect('databases/batteries_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO batteries '
            '(type, voltage, resistance) VALUES (?, ?, ?)',
            (battery_type, voltage, resistance)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get(battery_type: str) -> tuple:
        """
        Получает данные батареи по ее типу.
        Args:
            battery_type: Тип батареи.

        Returns:
            Тип, напряжение и сопротивление аккумуляторной батареи.

        """
        connection = sqlite3.connect('databases/batteries_database.db')
        cursor = connection.cursor()
        res = cursor.execute(
            'SELECT type, voltage, resistance FROM batteries WHERE type=?',
            (battery_type,)
        ).fetchone()
        connection.close()
        return res

    @staticmethod
    def delete(battery_type: str):
        """
        Удаляет запись по типу батареи.
        Args:
            battery_type: Тип батареи

        """
        connection = sqlite3.connect('databases/batteries_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM batteries WHERE type=?',
            (battery_type,)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def update(battery_type: str, voltage=None, resistance=None):
        """
        Обновляет запись по типу батареи.
        Args:
            battery_type: Тип аккумуляторной батареи для обновления.
            voltage: Напряжение аккумуляторной батареи, которое
            требуется обновить.
            resistance: Сопротивление аккумуляторной батареи, которое
            требуется обновить.

        """
        connection = sqlite3.connect('databases/batteries_database.db')
        cursor = connection.cursor()
        cursor.execute("""
           UPDATE batteries
           SET voltage=?, resistance=?
           WHERE battery_type=?
        """, (voltage, resistance, battery_type))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all() -> list:
        """
        Получает полный список батарей в виде кортежей (type,
        voltage, resistance).

        Returns:
            Список записей в виде кортежей (type, voltage,
            resistance).

        """
        connection = sqlite3.connect('databases/batteries_database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM batteries')
        all_batteries = cursor.fetchall()
        return all_batteries


class CablesDataBase:
    """
    Класс для работы с базой кабелей.

    """

    @staticmethod
    def add(cable_type: str, cross_section: float, length: float):
        """
        Добавляет кабель в базу.
        Args:
            cable_type: Тип кабеля.
            cross_section: Сечение.
            length: Длина.

        """
        connection = sqlite3.connect('databases/cables_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO cables (type, section, length) VALUES (?, ?, ?)',
            (cable_type, cross_section, length)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get(cable_type: str) -> tuple:
        connection = sqlite3.connect('databases/cables_database.db')
        cursor = connection.cursor()
        cable_res = cursor.execute(
            'SELECT type, section, length FROM cables WHERE type=?',
            (cable_type,)
        ).fetchone()
        connection.close()
        return cable_res

    @staticmethod
    def delete(cable_type: str):
        connection = sqlite3.connect('databases/cables_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM cables WHERE type=?',
            (cable_type,)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def update(cable_type: str, cross_section: float, length: float):
        connection = sqlite3.connect('databases/cables_database.db')
        cursor = connection.cursor()
        cursor.execute("""
           UPDATE cables
           SET section=?, length=?
           WHERE type=?
        """, (cross_section, length, cable_type))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all() -> list:
        connection = sqlite3.connect('databases/cables_database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM cables')
        all_cables = cursor.fetchall()
        return all_cables


class BreakersDataBase:
    """
    Класс для работы с базой выключателей.

    """

    @staticmethod
    def add(breaker_type: str, ibreak: float, tbreak: float):
        """
        Добавляет выключатель в базу.
        Args:
            breaker_type: Тип выключателя.
            ibreak: Ток срабатывания.
            tbreak: Время срабатывания.

        """
        connection = sqlite3.connect('databases/breakers_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO breakers (type, ibreak, tbreak) VALUES (?, ?, ?)',
            (breaker_type, ibreak, tbreak)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get(breaker_type: str) -> tuple:
        connection = sqlite3.connect('databases/breakers_database.db')
        cursor = connection.cursor()
        breaker_res = cursor.execute(
            'SELECT type, ibreak, tbreak FROM breakers WHERE type=?',
            (breaker_type,)
        ).fetchone()
        connection.close()
        return breaker_res

    @staticmethod
    def delete(breaker_type: str):
        connection = sqlite3.connect('databases/breakers_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM breakers WHERE type=?',
            (breaker_type,)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def update(breaker_type: str, ibreak: float, tbreak: float):
        connection = sqlite3.connect('databases/breakers_database.db')
        cursor = connection.cursor()
        cursor.execute("""
           UPDATE breakers
           SET ibreak=?, tbreak=?
           WHERE type=?
        """, (ibreak, tbreak, breaker_type))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all() -> list:
        connection = sqlite3.connect('databases/breakers_database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM breakers')
        all_breakers = cursor.fetchall()
        return all_breakers


class FusesDataBase:
    """
    Класс для работы с базой предохранителей.

    """

    @staticmethod
    def add(fuse_type: str, inom: float, tnom: float):
        """
        Добавляет предохранитель в базу.
        Args:
            fuse_type: Тип предохранителя.
            inom: Ток предохранителя.
            tnom: Время срабатывания предохранителя.

        """
        connection = sqlite3.connect('databases/fuses_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO fuses (type, inom, tnom) VALUES (?, ?, ?)',
            (fuse_type, inom, tnom)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get(fuse_type: str) -> tuple:
        connection = sqlite3.connect('databases/fuses_database.db')
        cursor = connection.cursor()
        fuse_res = cursor.execute(
            'SELECT type, inom, tnom FROM fuses WHERE type=?',
            (fuse_type,)
        ).fetchone()
        connection.close()
        return fuse_res

    @staticmethod
    def delete(fuse_type: str):
        connection = sqlite3.connect('databases/fuses_database.db')
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM fuses WHERE type=?',
            (fuse_type,)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def update(fuse_type: str, inom: float, tnom: float):
        connection = sqlite3.connect('databases/fuses_database.db')
        cursor = connection.cursor()
        cursor.execute("""
           UPDATE fuses
           SET inom=?, tnom=?
           WHERE type=?
        """, (inom, tnom, fuse_type))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all() -> list:
        connection = sqlite3.connect('databases/fuses_database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM fuses')
        all_fuses = cursor.fetchall()
        return all_fuses
