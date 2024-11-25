import sys

from PyQt6.QtWidgets import QApplication

from calc_db_create import (create_batteries_database,
                            create_breakers_database,
                            create_fuses_database,
                            create_cables_database)
from calc_ui import MainWindow

if __name__ == '__main__':
    # Создаем пустые базы оборудования для дальнейшей работы,
    # если не созданы ранее.
    create_batteries_database()
    create_breakers_database()
    create_fuses_database()
    create_cables_database()

    # Запускаем графический интерфейс
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
