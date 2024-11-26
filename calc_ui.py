from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QMainWindow, QLabel, QWidget, QGridLayout,
                             QPushButton, QLineEdit, QComboBox,
                             QVBoxLayout, QTableWidget)

from calc_calculation import Battery, Cable, Breaker, Fuse, calculation
from calc_db_work import (BatteriesDataBase, CablesDataBase,
                          BreakersDataBase, FusesDataBase)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fuse_from_db = None
        self.br_from_db = None
        self.cab_from_db = None
        self.bat_from_db = None
        self.setWindowTitle('Программа расчета токов')

        # Создаем сеточный макет основного экрана
        self.layout = QGridLayout()

        self.label_main = QLabel('Выберите вариант схемы')
        self.set_label_font(self.label_main, 15)
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_main, 0, 0, 1, 3)

        self.label_1 = QLabel('Вариант 1')
        self.set_label_font(self.label_1, 15)
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_2 = QLabel('Вариант 2')
        self.set_label_font(self.label_2, 15)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_3 = QLabel('Вариант 3')
        self.set_label_font(self.label_3, 15)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label_1, 1, 0)
        self.layout.addWidget(self.label_2, 1, 1)
        self.layout.addWidget(self.label_3, 1, 2)

        self.label_image_1 = QLabel(self)
        self.image_1 = QPixmap('images/image_1.jpg')
        self.label_image_1.setPixmap(self.image_1)
        self.resize(self.image_1.width(), self.image_1.height())
        self.label_image_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_image_2 = QLabel(self)
        self.image_2 = QPixmap('images/image_2.jpg')
        self.label_image_2.setPixmap(self.image_2)
        self.resize(self.image_2.width(), self.image_2.height())
        self.label_image_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_image_3 = QLabel(self)
        self.image_3 = QPixmap('images/image_3.jpg')
        self.label_image_3.setPixmap(self.image_3)
        self.resize(self.image_3.width(), self.image_3.height())
        self.label_image_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label_image_1, 2, 0)
        self.layout.addWidget(self.label_image_2, 2, 1)
        self.layout.addWidget(self.label_image_3, 2, 2)

        # Кнопки выбора варианта схемы для расчета.
        # По нажатию на экран будет выводиться
        # обновленный макет с выбранной схемой и блоками ввода данных.
        self.button_1 = QPushButton('Выбрать')
        self.button_1.adjustSize()
        self.button_1.setObjectName('Вариант 1')
        self.button_1.clicked.connect(self.renew_layout)  # type: ignore

        self.button_2 = QPushButton('Выбрать')
        self.button_2.adjustSize()
        self.button_2.setObjectName('Вариант 2')
        self.button_2.clicked.connect(self.renew_layout)  # type: ignore

        self.button_3 = QPushButton('Выбрать')
        self.button_3.adjustSize()
        self.button_3.setObjectName('Вариант 3')
        self.button_3.clicked.connect(self.renew_layout)  # type: ignore

        self.layout.addWidget(self.button_1, 3, 0)
        self.layout.addWidget(self.button_2, 3, 1)
        self.layout.addWidget(self.button_3, 3, 2)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.showMaximized()

    def renew_layout(self):
        """
        Метод обновляет макет главного окна, выводя
        на экран выбранную схему, блоки ввода данных,
        выбора элементов из базы.

        """
        # Очистка элементов предыдущего экрана
        self.label_main.deleteLater()
        self.label_1.deleteLater()
        self.label_2.deleteLater()
        self.label_3.deleteLater()
        self.button_1.deleteLater()
        self.button_2.deleteLater()
        self.button_3.deleteLater()
        self.label_image_1.deleteLater()
        self.label_image_2.deleteLater()
        self.label_image_3.deleteLater()

        # Принимаем сигнал о выбранном варианте от соответствующей кнопки.
        self.chosen_scheme = self.sender().objectName()

        # В обновленном макете задаем верхнее поле с заголовками.
        self.label_main = QLabel('Ввод исходных данных')
        self.set_label_font(self.label_main, 18)
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_main, 0, 0, 1, 3)

        self.label_1 = QLabel(f'Расчетная схема: {self.chosen_scheme}')
        self.set_label_font(self.label_1, 14)
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_1, 1, 0)

        self.label_2 = QLabel('Имя оборудования')
        self.set_label_font(self.label_2, 14)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_2, 1, 1)

        self.label_3 = QLabel('Параметры оборудования')
        self.set_label_font(self.label_3, 14)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_3, 1, 2)

        self.label_4 = QLabel('Выбор из базы')
        self.set_label_font(self.label_4, 14)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_4, 1, 3)

        # Выводим на экран схему выбранного варианта. Для выбранного
        # варианта отображаем в нужной последовательности блоки ввода
        # данных для элементов.
        self.label_chosen_image = QLabel(self)
        match self.chosen_scheme:
            case 'Вариант 1':
                self.chosen_image = QPixmap('images/image_1.jpg')
                self.set_battery(1)
                self.set_cable(2)
                self.set_breaker(3)
            case 'Вариант 2':
                self.chosen_image = QPixmap('images/image_2.jpg')
                self.set_battery(1)
                self.set_cable(2)
                self.set_fuse(3)
            case 'Вариант 3':
                self.chosen_image = QPixmap('images/image_3.jpg')
                self.set_battery(1)
                self.set_fuse(2)
                self.set_cable(3)

        self.label_chosen_image.setPixmap(self.chosen_image)
        self.resize(self.chosen_image.width(),
                    self.chosen_image.height()
                    )
        self.label_chosen_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_chosen_image, 2, 0, 4, 1)

        # Задаем общие для каждого варианта элементы. Для гибкости
        # дальнейшего расширения функционала применяем сеточный макет
        # QGridLayout для каждого поля внутри общего сеточного макета
        # всего окна.
        self.grid_el4_col1 = QGridLayout()
        self.label_el4 = QLabel('Короткое замыкание')
        self.set_label_font(self.label_el4, 10)
        self.grid_el4_col1.addWidget(self.label_el4, 0, 0)
        self.box_el4 = QComboBox()
        self.box_el4.addItems(["Металлическое замыкание", "Дуговое замыкание"])
        self.grid_el4_col1.addWidget(self.box_el4, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.grid_el4_col1, 5, 1)

        self.button_calc = QPushButton('Выполнить расчет')
        self.button_calc.adjustSize()
        self.button_calc.setObjectName('Выполнить расчет')
        self.button_calc.clicked.connect(self.make_calc)  # type: ignore
        self.layout.addWidget(self.button_calc, 5, 2, 2, 2)

    def set_battery(self, num_of_element: int):
        """Создает графический интерфейс для элемента Батарея.

        Args:
            num_of_element: Порядковый номер элемента на схеме

        """
        self.bat_num = num_of_element + 1

        # Определяем ячейки для элемента 1.
        # Определяем текстовую метку, отображающую имя элемента
        # в столбце 2:
        self.label_bat_name = QLabel()

        # Определяем ячейку элемента 1 в столбце 1 "Ввод наименования
        # оборудования". Создаем в ячейке внутреннюю таблицу для
        # возможности расширения функционала в будущем
        self.grid_bat_col1 = QGridLayout()
        # Определяем ячейки этой таблицы
        self.label_bat = QLabel('Аккумуляторная батарея\n'
                                'Имя элемента:')
        self.set_label_font(self.label_bat, 10)
        self.grid_bat_col1.addWidget(
            self.label_bat, 0, 0,
            Qt.AlignmentFlag.AlignBottom)
        self.input_bat = QLineEdit()
        self.set_label_font(self.input_bat, 10)
        # Введенный текст передаем в столбец 2:
        self.input_bat.textChanged.connect(         # type: ignore
            self.label_bat_name.setText)
        self.grid_bat_col1.addWidget(self.input_bat, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.grid_bat_col1, self.bat_num, 1)

        # Определяем ячейку элемента 1 в столбце 2 "Ввод
        # параметров оборудования".
        # Определяем сетку ячейки элемента 1:
        self.grid_bat_col2 = QGridLayout()
        # Заполняем сетку ячейки виджетами:
        self.label_bat_name_col2 = QLabel('Имя:')
        self.set_label_font(self.label_bat_name_col2, 10)
        self.grid_bat_col2.addWidget(self.label_bat_name_col2, 0, 0)
        # self.label_bat_name определено выше, включаем его в столбец 2
        self.set_label_font(self.label_bat_name, 10)
        self.grid_bat_col2.addWidget(self.label_bat_name, 0, 1)

        self.label_bat_type = QLabel('Тип:')
        self.set_label_font(self.label_bat_type, 10)
        self.grid_bat_col2.addWidget(self.label_bat_type, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)

        self.input_bat_type = QLineEdit()
        self.set_label_font(self.input_bat_type, 10)
        self.grid_bat_col2.addWidget(self.input_bat_type, 1, 1,
                                     Qt.AlignmentFlag.AlignTop)

        self.label_bat_param1 = QLabel('Напряжение, В:')
        self.set_label_font(self.label_bat_param1, 10)
        self.grid_bat_col2.addWidget(self.label_bat_param1, 2, 0,
                                     Qt.AlignmentFlag.AlignTop)

        self.input_bat_param1 = QLineEdit()
        self.set_label_font(self.input_bat_param1, 10)
        self.grid_bat_col2.addWidget(self.input_bat_param1, 2, 1,
                                     Qt.AlignmentFlag.AlignTop)

        self.label_bat_param2 = QLabel('Сопротивление, Ом:')
        self.set_label_font(self.label_bat_param2, 10)
        self.grid_bat_col2.addWidget(self.label_bat_param2, 3, 0,
                                     Qt.AlignmentFlag.AlignTop)

        self.input_bat_param2 = QLineEdit()
        self.set_label_font(self.input_bat_param2, 10)
        self.grid_bat_col2.addWidget(self.input_bat_param2, 3, 1,
                                     Qt.AlignmentFlag.AlignTop)

        self.button_bat_to_db = QPushButton('Внести батарею в базу')
        self.button_bat_to_db.adjustSize()
        self.button_bat_to_db.setObjectName('battery')
        self.button_bat_to_db.clicked.connect(  # type: ignore
            self.add_element_to_db)
        self.grid_bat_col2.addWidget(self.button_bat_to_db, 4, 0, 1, 2)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_bat_col2, self.bat_num, 2)

        # Определяем ячейку элемента 1 столбца 3 "Выбор оборудования из базы".
        # Определяем сетку ячейки элемента 1:
        self.grid_bat_col3 = QGridLayout()

        self.button_bat_from_db = QPushButton('Выбрать батарею из базы')
        self.button_bat_from_db.adjustSize()
        self.button_bat_from_db.setObjectName('battery')
        self.button_bat_from_db.clicked.connect(  # type: ignore
            self.get_element_from_db)
        self.grid_bat_col3.addWidget(self.button_bat_from_db, 0, 0)

        if self.bat_from_db is None:
            self.bat_type_from_db = QLabel('')
            self.bat_param1_from_db = QLabel('')
            self.bat_param2_from_db = QLabel('')

        self.set_label_font(self.bat_type_from_db, 10)
        self.bat_type_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.bat_param1_from_db, 10)
        self.bat_param1_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.bat_param2_from_db, 10)
        self.bat_param2_from_db.setStyleSheet("border: 1px solid black;")

        self.button_bat_dont_use_db = QPushButton('Отменить выбор батареи')
        self.button_bat_dont_use_db.adjustSize()
        self.button_bat_dont_use_db.setObjectName('battery')
        self.button_bat_dont_use_db.clicked.connect(    # type: ignore
            self.undone_from_db)

        self.grid_bat_col3.addWidget(self.bat_type_from_db, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.grid_bat_col3.addWidget(self.bat_param1_from_db, 2, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.grid_bat_col3.addWidget(self.bat_param2_from_db, 3, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.grid_bat_col3.addWidget(self.button_bat_dont_use_db, 4, 0,
                                     Qt.AlignmentFlag.AlignTop)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_bat_col3, self.bat_num, 3)

    def set_cable(self, num_of_element: int):
        """Создает графический интерфейс для элемента Кабель.

        Args:
            num_of_element: Порядковый номер элемента на схеме

        """
        self.cab_num = num_of_element + 1

        # Определяем ячейки для элемента 1.
        # Определяем текстовую метку, отображающую имя элемента в столбце 2:
        self.label_cab_name = QLabel()

        # Определяем ячейку элемента 1 в столбце 1 "Ввод наименования
        # оборудования". Создаем в ячейке внутреннюю таблицу для
        # возможности расширения функционала в будущем
        self.grid_cab_col1 = QGridLayout()
        # Определяем ячейки этой таблицы
        self.label_cab = QLabel('Кабель\n'
                                'Имя элемента:')
        self.set_label_font(self.label_cab, 10)
        self.grid_cab_col1.addWidget(self.label_cab, 0, 0,
                                     Qt.AlignmentFlag.AlignBottom)
        self.input_cab = QLineEdit()
        self.set_label_font(self.input_cab, 10)
        # Введенный текст передаем в столбец 2:
        self.input_cab.textChanged.connect(  # type: ignore
            self.label_cab_name.setText)
        self.grid_cab_col1.addWidget(self.input_cab, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.grid_cab_col1, self.cab_num, 1)

        # Определяем ячейку элемента 1 в столбце 2
        # "Ввод параметров оборудования".
        # Определяем сетку ячейки элемента 1:
        self.grid_cab_col2 = QGridLayout()
        # Заполняем сетку ячейки виджетами:
        self.label_cab_name_col2 = QLabel('Имя:')
        self.set_label_font(self.label_cab_name_col2, 10)
        self.grid_cab_col2.addWidget(self.label_cab_name_col2, 0, 0)
        # self.label_cab_name определено выше, включаем его в столбец 2
        self.set_label_font(self.label_cab_name, 10)
        self.grid_cab_col2.addWidget(self.label_cab_name, 0, 1)

        self.label_cab_type = QLabel('Тип:')
        self.set_label_font(self.label_cab_type, 10)
        self.grid_cab_col2.addWidget(self.label_cab_type, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)

        self.input_cab_type = QLineEdit()
        self.set_label_font(self.input_cab_type, 10)
        self.grid_cab_col2.addWidget(self.input_cab_type, 1, 1,
                                     Qt.AlignmentFlag.AlignTop)

        self.label_cab_param1 = QLabel('Сечение, мм2:')
        self.set_label_font(self.label_cab_param1, 10)
        self.grid_cab_col2.addWidget(self.label_cab_param1, 2, 0,
                                     Qt.AlignmentFlag.AlignTop)

        self.input_cab_param1 = QLineEdit()
        self.set_label_font(self.input_cab_param1, 10)
        self.grid_cab_col2.addWidget(self.input_cab_param1, 2, 1,
                                     Qt.AlignmentFlag.AlignTop)

        self.label_cab_param2 = QLabel('Длина, м:')
        self.set_label_font(self.label_cab_param2, 10)
        self.grid_cab_col2.addWidget(self.label_cab_param2, 3, 0,
                                     Qt.AlignmentFlag.AlignTop)

        self.input_cab_param2 = QLineEdit()
        self.set_label_font(self.input_cab_param2, 10)
        self.grid_cab_col2.addWidget(self.input_cab_param2, 3, 1,
                                     Qt.AlignmentFlag.AlignTop)

        self.button_cab_to_db = QPushButton('Внести кабель в базу')
        self.button_cab_to_db.adjustSize()
        self.button_cab_to_db.setObjectName('cable')
        self.button_cab_to_db.clicked.connect(  # type: ignore
            self.add_element_to_db)
        self.grid_cab_col2.addWidget(self.button_cab_to_db, 4, 0, 1, 2)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_cab_col2, self.cab_num, 2)

        # Определяем ячейку элемента 1 в столбце 3
        # "Выбор оборудования из базы".
        # Определяем сетку ячейки элемента 1:
        self.grid_cab_col3 = QGridLayout()

        self.button_cab_from_db = QPushButton('Выбрать кабель из базы')
        self.button_cab_from_db.adjustSize()
        self.button_cab_from_db.setObjectName('cable')
        self.button_cab_from_db.clicked.connect(  # type: ignore
            self.get_element_from_db)
        self.grid_cab_col3.addWidget(self.button_cab_from_db, 0, 0)

        if self.cab_from_db is None:
            self.cab_type_from_db = QLabel('')
            self.cab_param1_from_db = QLabel('')
            self.cab_param2_from_db = QLabel('')

        self.set_label_font(self.cab_type_from_db, 10)
        self.cab_type_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.cab_param1_from_db, 10)
        self.cab_param1_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.cab_param2_from_db, 10)
        self.cab_param2_from_db.setStyleSheet("border: 1px solid black;")

        self.button_cab_dont_use_db = QPushButton('Отменить выбор элемента')
        self.button_cab_dont_use_db.adjustSize()
        self.button_cab_dont_use_db.setObjectName('cable')
        self.button_cab_dont_use_db.clicked.connect(  # type: ignore
            self.undone_from_db)

        self.grid_cab_col3.addWidget(self.cab_type_from_db, 1, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.grid_cab_col3.addWidget(self.cab_param1_from_db, 2, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.grid_cab_col3.addWidget(self.cab_param2_from_db, 3, 0,
                                     Qt.AlignmentFlag.AlignTop)
        self.grid_cab_col3.addWidget(self.button_cab_dont_use_db, 4, 0,
                                     Qt.AlignmentFlag.AlignTop)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_cab_col3, self.cab_num, 3)

    def set_breaker(self, num_of_element: int):
        """Создает графический интерфейс для элемента Выключатель.

        Args:
            num_of_element: Порядковый номер элемента на схеме

        """
        self.br_num = num_of_element + 1

        # Определяем ячейки для элемента 1.
        # Определяем текстовую метку, отображающую имя элемента в столбце 2:
        self.label_br_name = QLabel()

        # Определяем ячейку элемента 1 в столбце 1
        # "Ввод наименования оборудования".
        # Создаем в ячейке внутреннюю таблицу для возможности
        # расширения функционала в будущем
        self.grid_br_col1 = QGridLayout()
        # Определяем ячейки этой таблицы
        self.label_br = QLabel('Выключатель\n'
                               'Имя элемента:')
        self.set_label_font(self.label_br, 10)
        self.grid_br_col1.addWidget(self.label_br, 0, 0,
                                    Qt.AlignmentFlag.AlignBottom)
        self.input_br = QLineEdit()
        self.set_label_font(self.input_br, 10)
        # Введенный текст передаем в столбец 2:
        self.input_br.textChanged.connect(  # type: ignore
            self.label_br_name.setText)
        self.grid_br_col1.addWidget(self.input_br, 1, 0,
                                    Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.grid_br_col1, self.br_num, 1)

        # Определяем ячейку элемента 1 в столбце 2
        # "Ввод параметров оборудования".
        # Определяем сетку ячейки элемента 1:
        self.grid_br_col2 = QGridLayout()
        # Заполняем сетку ячейки виджетами:
        self.label_br_name_col2 = QLabel('Имя:')
        self.set_label_font(self.label_br_name_col2, 10)
        self.grid_br_col2.addWidget(self.label_br_name_col2, 0, 0)
        # self.label_br_name определено выше, включаем его в столбец 2
        self.set_label_font(self.label_br_name, 10)
        self.grid_br_col2.addWidget(self.label_br_name, 0, 1)

        self.label_br_type = QLabel('Тип:')
        self.set_label_font(self.label_br_type, 10)
        self.grid_br_col2.addWidget(self.label_br_type, 1, 0,
                                    Qt.AlignmentFlag.AlignTop)

        self.input_br_type = QLineEdit()
        self.set_label_font(self.input_br_type, 10)
        self.grid_br_col2.addWidget(self.input_br_type, 1, 1,
                                    Qt.AlignmentFlag.AlignTop)

        self.label_br_param1 = QLabel('Ток срабатывания, А')
        self.set_label_font(self.label_br_param1, 10)
        self.grid_br_col2.addWidget(self.label_br_param1, 2, 0,
                                    Qt.AlignmentFlag.AlignTop)

        self.input_br_param1 = QLineEdit()
        self.set_label_font(self.input_br_param1, 10)
        self.grid_br_col2.addWidget(self.input_br_param1, 2, 1,
                                    Qt.AlignmentFlag.AlignTop)

        self.label_br_param2 = QLabel('Время срабатывания, с:')
        self.set_label_font(self.label_br_param2, 10)
        self.grid_br_col2.addWidget(self.label_br_param2, 3, 0,
                                    Qt.AlignmentFlag.AlignTop)

        self.input_br_param2 = QLineEdit()
        self.set_label_font(self.input_br_param2, 10)
        self.grid_br_col2.addWidget(self.input_br_param2, 3, 1,
                                    Qt.AlignmentFlag.AlignTop)

        self.button_br_to_db = QPushButton('Внести выключатель в базу')
        self.button_br_to_db.adjustSize()
        self.button_br_to_db.setObjectName('breaker')
        self.button_br_to_db.clicked.connect(  # type: ignore
            self.add_element_to_db)
        self.grid_br_col2.addWidget(self.button_br_to_db, 4, 0, 1, 2)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_br_col2, self.br_num, 2)

        # Определяем ячейку элемента 1 в столбце 3
        # "Выбор оборудования из базы".
        # Определяем сетку ячейки элемента 1:
        self.grid_br_col3 = QGridLayout()

        self.button_br_from_db = QPushButton('Выбрать выключатель из базы')
        self.button_br_from_db.adjustSize()
        self.button_br_from_db.setObjectName('breaker')
        self.button_br_from_db.clicked.connect(  # type: ignore
            self.get_element_from_db)
        self.grid_br_col3.addWidget(self.button_br_from_db, 0, 0)

        if self.br_from_db is None:
            self.br_type_from_db = QLabel('')
            self.br_param1_from_db = QLabel('')
            self.br_param2_from_db = QLabel('')

        self.set_label_font(self.br_type_from_db, 10)
        self.br_type_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.br_param1_from_db, 10)
        self.br_param1_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.br_param2_from_db, 10)
        self.br_param2_from_db.setStyleSheet("border: 1px solid black;")

        self.button_br_dont_use_db = QPushButton('Отменить выбор выключателя')
        self.button_br_dont_use_db.adjustSize()
        self.button_br_dont_use_db.setObjectName('breaker')
        self.button_br_dont_use_db.clicked.connect(  # type: ignore
            self.undone_from_db)

        self.grid_br_col3.addWidget(self.br_type_from_db, 1, 0,
                                    Qt.AlignmentFlag.AlignTop)
        self.grid_br_col3.addWidget(self.br_param1_from_db, 2, 0,
                                    Qt.AlignmentFlag.AlignTop)
        self.grid_br_col3.addWidget(self.br_param2_from_db, 3, 0,
                                    Qt.AlignmentFlag.AlignTop)
        self.grid_br_col3.addWidget(self.button_br_dont_use_db, 4, 0,
                                    Qt.AlignmentFlag.AlignTop)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_br_col3, self.br_num, 3)

    def set_fuse(self, num_of_element: int):
        """Создает графический интерфейс для элемента Предохранитель.

        Args:
            num_of_element: Порядковый номер элемента на схеме

        """
        self.fuse_num = num_of_element + 1

        # Определяем ячейки для элемента 1.
        # Определяем текстовую метку, отображающую
        # имя элемента в столбце 2:
        self.label_fuse_name = QLabel()

        # Определяем ячейку элемента 1 в столбце 1 "Ввод наименования
        # оборудования". Создаем в ячейке внутреннюю таблицу для
        # возможности расширения функционала в будущем
        self.grid_fuse_col1 = QGridLayout()
        # Определяем ячейки этой таблицы
        self.label_fuse = QLabel('Предохранитель\n'
                                 'Имя элемента:')
        self.set_label_font(self.label_fuse, 10)
        self.grid_fuse_col1.addWidget(self.label_fuse, 0, 0,
                                      Qt.AlignmentFlag.AlignBottom)
        self.input_fuse = QLineEdit()
        self.set_label_font(self.input_fuse, 10)
        # Введенный текст передаем в столбец 2:
        self.input_fuse.textChanged.connect(  # type: ignore
            self.label_fuse_name.setText)
        self.grid_fuse_col1.addWidget(self.input_fuse, 1, 0,
                                      Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.grid_fuse_col1, self.fuse_num, 1)

        # Определяем ячейку элемента 1 в столбце 2
        # "Ввод параметров оборудования".
        # Определяем сетку ячейки элемента 1:
        self.grid_fuse_col2 = QGridLayout()
        # Заполняем сетку ячейки виджетами:
        self.label_fuse_name_col2 = QLabel('Имя:')
        self.set_label_font(self.label_fuse_name_col2, 10)
        self.grid_fuse_col2.addWidget(self.label_fuse_name_col2, 0, 0)
        # self.label_fuse_name определено выше, включаем его в столбец 2
        self.set_label_font(self.label_fuse_name, 10)
        self.grid_fuse_col2.addWidget(self.label_fuse_name, 0, 1)

        self.label_fuse_type = QLabel('Тип:')
        self.set_label_font(self.label_fuse_type, 10)
        self.grid_fuse_col2.addWidget(self.label_fuse_type, 1, 0,
                                      Qt.AlignmentFlag.AlignTop)

        self.input_fuse_type = QLineEdit()
        self.set_label_font(self.input_fuse_type, 10)
        self.grid_fuse_col2.addWidget(self.input_fuse_type, 1, 1,
                                      Qt.AlignmentFlag.AlignTop)

        self.label_fuse_param1 = QLabel('Номинальный ток, А')
        self.set_label_font(self.label_fuse_param1, 10)
        self.grid_fuse_col2.addWidget(self.label_fuse_param1, 2, 0,
                                      Qt.AlignmentFlag.AlignTop)

        self.input_fuse_param1 = QLineEdit()
        self.set_label_font(self.input_fuse_param1, 10)
        self.grid_fuse_col2.addWidget(self.input_fuse_param1, 2, 1,
                                      Qt.AlignmentFlag.AlignTop)

        self.label_fuse_param2 = QLabel('Номинальное время, с:')
        self.set_label_font(self.label_fuse_param2, 10)
        self.grid_fuse_col2.addWidget(self.label_fuse_param2, 3, 0,
                                      Qt.AlignmentFlag.AlignTop)

        self.input_fuse_param2 = QLineEdit()
        self.set_label_font(self.input_fuse_param2, 10)
        self.grid_fuse_col2.addWidget(self.input_fuse_param2, 3, 1,
                                      Qt.AlignmentFlag.AlignTop)

        self.button_fuse_to_db = QPushButton('Внести предохранитель в базу')
        self.button_fuse_to_db.adjustSize()
        self.button_fuse_to_db.setObjectName('fuse')
        self.button_fuse_to_db.clicked.connect(  # type: ignore
            self.add_element_to_db)
        self.grid_fuse_col2.addWidget(self.button_fuse_to_db, 4, 0, 1, 2)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_fuse_col2, self.fuse_num, 2)

        # Определяем ячейку элемента 1 столбца 3 "Выбор оборудования из базы".
        # Определяем сетку ячейки элемента 1:
        self.grid_fuse_col3 = QGridLayout()

        self.button_fuse_from_db = (
            QPushButton('Выбрать предохранитель из базы'))
        self.button_fuse_from_db.adjustSize()
        self.button_fuse_from_db.setObjectName('fuse')
        self.button_fuse_from_db.clicked.connect(  # type: ignore
            self.get_element_from_db)
        self.grid_fuse_col3.addWidget(self.button_fuse_from_db, 0, 0)

        if self.fuse_from_db is None:
            self.fuse_type_from_db = QLabel('')
            self.fuse_param1_from_db = QLabel('')
            self.fuse_param2_from_db = QLabel('')

        self.set_label_font(self.fuse_type_from_db, 10)
        self.fuse_type_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.fuse_param1_from_db, 10)
        self.fuse_param1_from_db.setStyleSheet("border: 1px solid black;")
        self.set_label_font(self.fuse_param2_from_db, 10)
        self.fuse_param2_from_db.setStyleSheet("border: 1px solid black;")

        self.button_fuse_dont_use_db = (
            QPushButton('Отменить выбор предохранителя'))
        self.button_fuse_dont_use_db.adjustSize()
        self.button_fuse_dont_use_db.setObjectName('fuse')
        self.button_fuse_dont_use_db.clicked.connect(  # type: ignore
            self.undone_from_db)

        self.grid_fuse_col3.addWidget(self.fuse_type_from_db, 1, 0,
                                      Qt.AlignmentFlag.AlignTop)
        self.grid_fuse_col3.addWidget(self.fuse_param1_from_db, 2, 0,
                                      Qt.AlignmentFlag.AlignTop)
        self.grid_fuse_col3.addWidget(self.fuse_param2_from_db, 3, 0,
                                      Qt.AlignmentFlag.AlignTop)
        self.grid_fuse_col3.addWidget(self.button_fuse_dont_use_db, 4, 0,
                                      Qt.AlignmentFlag.AlignTop)

        # Вносим ячейку в общий макет:
        self.layout.addLayout(self.grid_fuse_col3, self.fuse_num, 3)

    def make_calc(self):
        """
        Поверяет введенные параметры, фиксирует их и
        выполняет расчет тока и других параметров. При некорректном
        вводе данных выводит дополнительные окна-виджеты с информацией.
        После проверки создает объекты классов (обращение к модулю
        calc_calculation) и используя эти объекты вызывает из модуля
        calc_calculation функцию выполнения расчета.
        Результат выводит в отдельном окне.

        Returns: None (в случае некорректного ввода данных)

        """
        # Фиксируем параметры каждого элемента.
        # Фиксируем имя батареи, если оно не пустое.
        self.final_bat_name = self.input_bat.text().strip()
        if self.final_bat_name == '':
            self.window_extra = WindowCheckIfNameEmpty()
            self.window_extra.show()
            return
        # Фиксируем параметры батареи - выбранные из базы или заданные вручную.
        # С помощью функции check_data_to_use убираем неопределенность какие
        # данные использовать, если пользователь ввел вручную и выбрал из базы.
        # В итоге получаем объект класса с введенными данным.
        # Значения введенные в ручную:
        self.list_of_inputs_bat = [self.input_bat_type.text(),
                                   self.input_bat_param1.text(),
                                   self.input_bat_param2.text()]
        self.bat_to_check = self.check_data_to_use(
            self.list_of_inputs_bat, self.bat_from_db)
        if self.bat_to_check is False:
            return
        else:
            self.bat_final = Battery(self.final_bat_name, *self.bat_to_check)

        # Аналогичные действия (см. выше для батареи) выполняем
        # для каждого элемента.
        # Для кабеля.
        self.final_cab_name = self.input_cab.text().strip()
        if self.final_cab_name == '':
            self.window_extra = WindowCheckIfNameEmpty()
            self.window_extra.show()
            return
        self.list_of_inputs_cab = [self.input_cab_type.text(),
                                   self.input_cab_param1.text(),
                                   self.input_cab_param2.text()]
        self.cab_to_check = self.check_data_to_use(
            self.list_of_inputs_cab, self.cab_from_db)
        if self.cab_to_check is False:
            return
        else:
            self.cab_final = Cable(self.final_cab_name, *self.cab_to_check)

        # Для выключателя (если он присутствует в схеме).
        if self.chosen_scheme == 'Вариант 1':
            self.final_br_name = self.input_br.text().strip()
            if self.final_br_name == '':
                self.window_extra = WindowCheckIfNameEmpty()
                self.window_extra.show()
                return
            self.list_of_inputs_br = [self.input_br_type.text(),
                                      self.input_br_param1.text(),
                                      self.input_br_param2.text()]
            self.br_to_check = self.check_data_to_use(self.list_of_inputs_br,
                                                      self.br_from_db)
            if self.br_to_check is False:
                return
            else:
                self.br_final = Breaker(self.final_br_name, *self.br_to_check)

        # Для предохранителя (если он присутствует в схеме).
        if (self.chosen_scheme == 'Вариант 2'
                or self.chosen_scheme == 'Вариант 3'):
            self.final_fuse_name = self.input_fuse.text().strip()
            if self.final_fuse_name == '':
                self.window_extra = WindowCheckIfNameEmpty()
                self.window_extra.show()
                return
            self.list_of_inputs_fuse = [self.input_fuse_type.text(),
                                        self.input_fuse_param1.text(),
                                        self.input_fuse_param2.text()]
            self.fuse_to_check = self.check_data_to_use(
                self.list_of_inputs_fuse, self.fuse_from_db)
            if self.fuse_to_check is False:
                return
            else:
                self.fuse_final = Fuse(self.final_fuse_name,
                                       *self.fuse_to_check)

        self.type_of_current = self.box_el4.currentText()

        if self.chosen_scheme == 'Вариант 1':
            self.calc = calculation(self.bat_final,
                                    self.cab_final,
                                    self.type_of_current,
                                    breaker=self.br_final)
            self.window_final = WindowFinalCalc(self.calc)
            self.window_final.show()

        if self.chosen_scheme == 'Вариант 2':
            self.calc = calculation(self.bat_final,
                                    self.cab_final,
                                    self.type_of_current,
                                    fuse=self.fuse_final)
            self.window_final = WindowFinalCalc(self.calc)
            self.window_final.show()

        if self.chosen_scheme == 'Вариант 3':
            self.calc = calculation(self.bat_final,
                                    self.cab_final,
                                    self.type_of_current,
                                    fuse=self.fuse_final
                                    )
            self.window_final = WindowFinalCalc(self.calc)
            self.window_final.show()

    def check_data_to_use(self, list_of_inputs: list, el_from_db: tuple):
        """
        Определяет какие данные мы должны взять для расчета -
        те, что пользователь задал вручную или из базы. Чтобы у пользователя
        не было неопределенности, какие данные попадают в расчет.
        Алгоритм такой:
        1) если не выбран вариант из базы и хотя бы одно поле не заполнено,
        то функция попросит пользователя все заполнить или выбрать из базы.
        2) если выбран элемент из базы, то поля ручного ввода должны
        быть пустыми.
        3) если хотим все задать вручную, то нужно отменить добавление
        из базы.

        Args:
            list_of_inputs: список значений из полей ручного ввода.
            el_from_db: кортеж с данными из базы.

        Returns:
            Список параметров оборудования проверенный по алгоритму данной
            функции или False, если пользователь сделал что-то не так при
            вводе. При этом функция выводит дополнительные окна-виджеты с
            информацией о проблеме.

        """
        self.list_of_inputs_el = list_of_inputs
        self.el_from_db = el_from_db
        # Если хотя бы одно поле не заполнено и если не был
        # выбран элемент из базы, то просим пользователя что-то внести:
        if (
                any(v == '' for v in self.list_of_inputs_el) and
                self.el_from_db is None
        ):
            self.window_extra = WindowAllEmptyParams()
            self.window_extra.show()
            return False

        # Если заполнены поля (даже одно) вручную и был выбран элемент
        # из базы, то сообщим пользователю, что выбрать нужно что-то одно.
        elif (
                any(v != '' for v in self.list_of_inputs_el) and
                self.el_from_db is not None
        ):
            self.window_extra = WindowRedundantParams()
            self.window_extra.show()
            return False

        # Если был выбран элемент из базы и поля пустые,
        # то окончательно берем тот, что из базы:
        elif (
                self.el_from_db is not None and
                all(v == '' for v in self.list_of_inputs_el)
        ):
            self.final_el_type = self.el_from_db[0]
            self.final_el_param1 = self.el_from_db[1]
            self.final_el_param2 = self.el_from_db[2]
            return [self.final_el_type,
                    self.final_el_param1,
                    self.final_el_param2
                    ]

        # Если заполнены все поля вручную и не был выбран элемент из базы,
        # то берем то, что вручную. Проверив предварительно, нет ли ошибок
        # в полях ввода, а также меняем тип числовых параметров с str на float:
        elif (
                self.el_from_db is None and
                all(v != '' for v in self.list_of_inputs_el)
        ):
            self.checked = self.check_user_input_values_and_convert(
                *self.list_of_inputs_el)
            if self.checked is False:
                return False
            # Если нет ошибок, то возвращаем проверенный список
            # параметров элемента:
            else:
                return self.checked

    def add_element_to_db(self):
        """
        Добавляет элемент в базу, предварительно проверив
        параметры с помощью вызова другой функции.

        """
        self.chosen_el = self.sender().objectName()
        # Проверяем откуда вызвали добавление в базу:
        if self.chosen_el == 'battery':
            self.list_of_inputs = [self.input_bat_type.text(),
                                   self.input_bat_param1.text(),
                                   self.input_bat_param2.text()]
            base_to_add = BatteriesDataBase()

        elif self.chosen_el == 'cable':
            self.list_of_inputs = [self.input_cab_type.text(),
                                   self.input_cab_param1.text(),
                                   self.input_cab_param2.text()]
            base_to_add = CablesDataBase()

        elif self.chosen_el == 'breaker':
            self.list_of_inputs = [self.input_br_type.text(),
                                   self.input_br_param1.text(),
                                   self.input_br_param2.text()]
            base_to_add = BreakersDataBase()

        elif self.chosen_el == 'fuse':
            self.list_of_inputs = [self.input_fuse_type.text(),
                                   self.input_fuse_param1.text(),
                                   self.input_fuse_param2.text()]
            base_to_add = FusesDataBase()

        # Проверяем, что параметры введены без ошибок и
        # преобразуем тип числовых параметров из str во float:
        self.checked = self.check_user_input_values_and_convert(
            *self.list_of_inputs
        )
        if self.checked is False:
            return
        # Если нет ошибок ввода данных, то добавляем элемент
        # в соответствующую базу:
        else:
            # При условии, что элемента с таким типом уже нет в базе:
            if base_to_add.get(self.checked[0]) is None:
                base_to_add.add(*self.checked)
                self.window_added = WindowAddedToDataBase()
                self.window_added.show()
            else:
                self.window_added = WindowErrAddToDataBase()
                self.window_added.show()

    def check_user_input_values_and_convert(self, el_type: str,
                                            el_param1: str,
                                            el_param2: str) -> list | bool:
        """
        Проверяет введенные пользователем в полях ввода данные на предмет
        лишних пробелов, букв и символов в полях ввода чисел и др.
        Данные текстовых полей, где требуется, преобразует в тип float.
        Если пользователь допустил ошибки, то выводит дополнительные
        окна с информацией.
        Args:
            el_type: Тип элемента.
            el_param1: Параметр 1 элемента.
            el_param2: Параметр 2 элемента.

        Returns:
            Список проверенных, преобразованных значений или False, если
            пользователь ввел данные некорректно.

        """
        self.el_type = el_type.strip()
        self.el_param1 = el_param1.replace(",", ".").strip()
        self.el_param2 = el_param2.replace(",", ".").strip()
        if self.el_type == '':
            self.window_err = WindowErrInParams()
            self.window_err.show()
            return False
        else:
            try:
                self.el_param1 = float(self.el_param1)
                self.el_param2 = float(self.el_param2)
            except ValueError:
                self.window_err = WindowErrInParams()
                self.window_err.show()
                return False

        return [self.el_type, self.el_param1, self.el_param2]

    def get_element_from_db(self):
        """
        Промежуточный метод для добавления элемента из базы.
        Проверяет из какой части интерфейса вызвали добавление
        элемента и вызывает окно работы с соответствующей базой
        данных. В итоге функция принимает сигнал из этого окна,
        содержащий данные элемента из базы и вызывает функцию
        для добавления этих данных на основное окно.

        """
        self.needed_el = self.sender().objectName()
        # Проверяем откуда вызвали добавление из базы и
        # вызываем новое окно для работы с базой
        self.window_get_from_db = WindowGetFromDataBase(
            self.needed_el
        )
        self.window_get_from_db.signal_from.connect(   # type: ignore
            self.use_element_from_db
        )
        self.window_get_from_db.show()

    def use_element_from_db(self, element: tuple):
        """
        Метод обрабатывает сигнал из окна работы с базой и
        добавляет данные из базы, переданные с этим
        сигналом в главное окно.

        Args:
            element: Кортеж с данными из базы

        """
        # Проверяем из какой базы идет добавление элемента
        if self.needed_el == 'battery':
            self.bat_from_db = element
            self.bat_type_from_db.setText(self.bat_from_db[0])
            self.bat_param1_from_db.setText(str(self.bat_from_db[1]))
            self.bat_param2_from_db.setText(str(self.bat_from_db[2]))

        elif self.needed_el == 'cable':
            self.cab_from_db = element
            self.cab_type_from_db.setText(self.cab_from_db[0])
            self.cab_param1_from_db.setText(str(self.cab_from_db[1]))
            self.cab_param2_from_db.setText(str(self.cab_from_db[2]))

        elif self.needed_el == 'breaker':
            self.br_from_db = element
            self.br_type_from_db.setText(self.br_from_db[0])
            self.br_param1_from_db.setText(str(self.br_from_db[1]))
            self.br_param2_from_db.setText(str(self.br_from_db[2]))

        elif self.needed_el == 'fuse':
            self.fuse_from_db = element
            self.fuse_type_from_db.setText(self.fuse_from_db[0])
            self.fuse_param1_from_db.setText(str(self.fuse_from_db[1]))
            self.fuse_param2_from_db.setText(str(self.fuse_from_db[2]))

    def undone_from_db(self):
        """
        Метод отменяет добавление на главный экран данных элемента из базы.
        В базе элемент остается.

        """
        self.undone_el = self.sender().objectName()
        # Проверяем для какого элемента отменяем добавление из базы
        if self.undone_el == 'battery':
            self.bat_type_from_db.setText('')
            self.bat_param1_from_db.setText('')
            self.bat_param2_from_db.setText('')
            self.bat_from_db = None

        elif self.undone_el == 'cable':
            self.cab_type_from_db.setText('')
            self.cab_param1_from_db.setText('')
            self.cab_param2_from_db.setText('')
            self.cab_from_db = None

        elif self.undone_el == 'breaker':
            self.br_type_from_db.setText('')
            self.br_param1_from_db.setText('')
            self.br_param2_from_db.setText('')
            self.br_from_db = None

        elif self.undone_el == 'fuse':
            self.fuse_type_from_db.setText('')
            self.fuse_param1_from_db.setText('')
            self.fuse_param2_from_db.setText('')
            self.fuse_from_db = None

    def set_label_font(self, label, size: int):
        """
        Вспомогательная функция, задающая размер шрифта для виджета с надписью.

        Args:
            label: Виджет с надписью.
            size: Размер шрифта.

        """
        self.label = label
        self.font = self.label.font()
        self.font.setPointSize(size)
        self.label.setFont(self.font)


class WindowGetFromDataBase(QWidget):
    """
    Класс создает окно для вывода базы данных и выбора
    элемента для добавления на главный экран.

    """
    # Сигнал, с которым передадим в главное окно
    # информацию о выбранном элементе:
    signal_from = pyqtSignal(tuple)

    def __init__(self, needed_el):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('Выбор элемента из базы')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.needed_el = needed_el

        # Проверяем из какой базы нужен элемент
        if self.needed_el == 'battery':
            self.label_main = QLabel('Название базы: batteries_database.db')
            self.base_to_get = BatteriesDataBase()

        elif self.needed_el == 'cable':
            self.label_main = QLabel('Название базы: cables_database.db')
            self.base_to_get = CablesDataBase()

        elif self.needed_el == 'breaker':
            self.label_main = QLabel('Название базы: breakers_database.db')
            self.base_to_get = BreakersDataBase()

        elif self.needed_el == 'fuse':
            self.label_main = QLabel('Название базы: fuses_database.db')
            self.base_to_get = FusesDataBase()

        self.font_main = self.label_main.font()
        self.font_main.setPointSize(15)
        self.label_main.setFont(self.font_main)
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_main)

        self.all_elements = self.base_to_get.get_all()

        self.table_db = QTableWidget()
        self.table_db.setColumnCount(4)
        self.table_db.setRowCount(len(self.all_elements))
        self.table_db.setHorizontalHeaderLabels(["Header 1",
                                                 "Header 2",
                                                 "Header 3",
                                                 "Header 4"]
                                                )
        for i in range(len(self.all_elements)):
            self.type = QLabel(self.all_elements[i][1])
            self.table_db.setCellWidget(i, 0, self.type)

            self.param1 = QLabel(str(self.all_elements[i][2]))
            self.table_db.setCellWidget(i, 1, self.param1)

            self.param2 = QLabel(str(self.all_elements[i][3]))
            self.table_db.setCellWidget(i, 2, self.param2)

            self.button_choose_el = QPushButton(self.table_db)
            self.button_choose_el.setText('Выбрать')

            # Передаем тип выбранного элемента в функцию get_element:
            self.button_choose_el.setObjectName(self.all_elements[i][1])
            self.button_choose_el.clicked.connect(    # type: ignore
                self.get_element
            )

            self.table_db.setCellWidget(i, 3, self.button_choose_el)

        self.layout.addWidget(self.table_db)
        self.table_db.resizeColumnsToContents()

        self.button_exit = QPushButton('Выйти без добавления')
        self.button_exit.adjustSize()
        self.button_exit.setObjectName('Выйти без добавления')
        self.button_exit.clicked.connect(self.close)  # type: ignore
        self.layout.addWidget(self.button_exit)

    def get_element(self):
        """
        Отправляет сигнал с данными - кортежем, содержащим параметры элемента.
        """
        self.chosen_element_type = self.sender().objectName()
        self.element = self.base_to_get.get(self.chosen_element_type)
        self.signal_from.emit(self.element)  # type: ignore
        self.close()


class WindowFinalCalc(QWidget):
    """
    Окно с информацией о результатах расчета.
    """

    def __init__(self, result):
        super().__init__()
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle('Результаты расчета')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.result = '\n'.join(result)
        self.label = QLabel(self.result)
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)

        self.button1 = QPushButton('Вернуться к схеме')
        self.layout.addWidget(self.button1, Qt.AlignmentFlag.AlignCenter)
        self.button1.clicked.connect(self.close)  # type: ignore


# Ниже определены вспомогательные окна-виджеты,
# сообщающие пользователю о результатах его действий:

class WindowAddedToDataBase(QWidget):
    """
    Окно-уведомление об успешном добавлении элемента в базу.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 150, 150)
        self.layout = QVBoxLayout()
        self.label = QLabel("Элемент добавлен в базу")
        self.button = QPushButton('Закрыть окно')
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.close)  # type: ignore


class WindowErrAddToDataBase(QWidget):
    """
    Окно-уведомление о неуспешном добавлении элемента в базу.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Ошибка добавления в базу')
        self.layout = QVBoxLayout()
        self.label = QLabel("Тип элемента должен быть уникальным")
        self.button = QPushButton('Закрыть окно')
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.close)  # type: ignore


class WindowCheckIfNameEmpty(QWidget):
    """
    Окно-уведомление об том, что имена элементов не заполнены.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Проблема с именами элементов')
        self.layout = QVBoxLayout()
        self.label = QLabel("Проверьте заполнены ли все имена")
        self.button = QPushButton('Закрыть окно')
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.close)  # type: ignore


class WindowRedundantParams(QWidget):
    """
    Окно-уведомление о том, что и выбран элемент из базы и заданы значения.
    Просим пользователя эту неопределенность устранить.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Проблема с вводом данных')
        self.layout = QVBoxLayout()
        self.label = QLabel('Выбран и элемент из базы и '
                            'заполнены поля ввода данных вручную.\n'
                            'Либо отмените выбор элемента, либо '
                            'сделайте поля параметров пустыми.')
        self.button = QPushButton('Закрыть окно')
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.close)  # type: ignore


class WindowAllEmptyParams(QWidget):
    """
    Окно-уведомление о том, что не выбран элемент из базы и
    не заданы значения вручную.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Проблема с вводом данных')
        self.setGeometry(300, 300, 150, 150)
        self.layout = QVBoxLayout()
        self.label = QLabel('Проверьте, что заполнены все поля '
                            'параметров ввода данных\n'
                            'или убедитесь, что выбран элемент '
                            'из базы.')
        self.button = QPushButton('Закрыть окно')
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.close)  # type: ignore


class WindowErrInParams(QWidget):
    """
    Окно-уведомление об ошибке ввода данных в полях.
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Ошибка в полях ввода параметров')
        self.layout = QVBoxLayout()
        self.label = QLabel('Проверьте, что поле "Тип" не пустое '
                            'и в других полях нет ошибок\n'
                            '(например, лишние пробелы, знаки, '
                            'буквы в полях, где требуются числа,\n'
                            'пустые незаполненные поля и т.п.).')
        self.button = QPushButton('Закрыть окно')
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.close)  # type: ignore
