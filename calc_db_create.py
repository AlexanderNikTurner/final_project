import sqlite3


def create_batteries_database():
    connection = sqlite3.connect('batteries_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS batteries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(30) NOT NULL UNIQUE,
    voltage FLOAT NULL,
    resistance FLOAT NULL
    )
    ''')

    connection.commit()
    connection.close()


def create_breakers_database():
    connection = sqlite3.connect('breakers_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS breakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(30) NOT NULL UNIQUE,
    ibreak FLOAT NULL,
    tbreak FLOAT NULL
    )
    ''')

    connection.commit()
    connection.close()


def create_fuses_database():
    connection = sqlite3.connect('fuses_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(30) NOT NULL UNIQUE,
    inom FLOAT NULL,
    tnom FLOAT NULL
    )
    ''')

    connection.commit()
    connection.close()


def create_cables_database():
    connection = sqlite3.connect('cables_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(30) NOT NULL UNIQUE,
    section FLOAT NULL,
    length FLOAT NULL
    )
    ''')

    connection.commit()
    connection.close()
