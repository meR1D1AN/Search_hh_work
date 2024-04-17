import os
import psycopg2
from typing import List, Dict, Union, Tuple
from src.color.color import Color
from src.api.hh_api import get_vacancies_by_employer_ids

password = os.environ['SQLPASS']


def create_database(dbname: str) -> None:
    """
    Функция, которая создаёт базу данных с указанным именем в PostgreSQL
    """
    try:
        # Подключение к серверу PostgreSQL без указания базы данных
        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        # Создание курсора
        cur = conn.cursor()
        # Создание базы данных с введённым именем
        cur.execute(f"CREATE DATABASE {dbname}")
        # Закрытие курсора и соединения
        cur.close()
        conn.close()
        print(f"База данных {Color.GREEN}{dbname}{Color.END} создана успешно!")
    except psycopg2.errors.DuplicateDatabase:
        print(f"База данных {Color.RED}{dbname}{Color.END} уже существует!")


def create_tables(dbname: str) -> None:
    """
    Создает таблицы в указанной базе данных.
    Вызывает исключение:
        Exception: Если возникает ошибка при создании таблиц.
        psycopg2.DatabaseError: Если возникает ошибка при подключении к базе данных.
    Эта функция создает две таблицы в указанной базе данных: 'companies' и 'vacancies'. Таблица 'companies' имеет
    два столбца: 'company_id' (SERIAL PRIMARY KEY) и 'name' (VARCHAR(255) NOT NULL). Таблица 'vacancies' имеет
    шесть столбцов: 'vacancy_id' (SERIAL PRIMARY KEY), 'company_id' (INTEGER NOT NULL), 'title' (VARCHAR(255) NOT NULL),
    'salary_from' (VARCHAR(100)), 'salary_to' (VARCHAR(100)) и 'link' (VARCHAR(255) NOT NULL). Столбец 'company_id'
    в таблице 'vacancies' является внешним ключом, ссылающимся на столбец 'company_id' в таблице 'companies'.
    Функция подключается к базе данных, используя указанное имя базы данных, пользователя, пароль, хост и порт.
    Затем она выполняет SQL-команды для создания таблиц и фиксирует изменения. Если возникает ошибка при создании
    таблиц или подключении к базе данных, вызывается соответствующее исключение. Наконец, функция закрывает
    соединение с базой данных.
    """
    commands: List[str] = (
        """
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            salary_from VARCHAR(100),
            salary_to VARCHAR(100),
            link VARCHAR(255) NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )
        """
    )

    try:
        # Подключение к базе данных с введённым именем
        conn = psycopg2.connect(
            dbname=dbname,
            user="postgres",
            password=password,
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        # Создание таблиц
        for command in commands:
            cur.execute(command)
        # Закрытие курсора и коммит изменений
        cur.close()
        conn.commit()
        print(f"Таблицы успешно созданы в базе данных {Color.GREEN}{dbname}{Color.END}!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при создании таблиц: {Color.RED}{error}{Color.END}")
    finally:
        if conn is not None:
            conn.close()


def fill_tables(dbname: str, employer_ids: List[str]) -> None:
    """
    Заполняет таблицы в указанной базе данных данными, полученными из API.
    Вызывает:
        Exception: Если происходит ошибка при подключении к базе данных или выполнении запросов.
        psycopg2.DatabaseError: Если происходит ошибка при выполнении запросов к базе данных.
    Выводит:
        Сообщение об успешном добавлении данных в таблицы, если операция прошла успешно.
        Сообщение об ошибке, если произошла ошибка при добавлении данных.
    """
    vacancies: List[Dict[str, Union[str, int]]] = get_vacancies_by_employer_ids(employer_ids)

    try:
        # Подключение к базе данных с введённым именем
        conn = psycopg2.connect(
            dbname=dbname,
            user="postgres",
            password=password,
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Вставка данных о компаниях
        company_names: Dict[int, str] = {vac['employer']['id']: vac['employer']['name'] for vac in vacancies}
        company_data: List[Tuple[int, str]] = [(id, name) for id, name in company_names.items()]
        insert_query = "INSERT INTO companies (company_id, name) VALUES (%s, %s)"
        cur.executemany(insert_query, company_data)

        # Вставка данных о вакансиях
        vacancy_data: List[Tuple[int, int, str, str, str, str]] = []
        for vac in vacancies:
            vacancy_id = vac['id']
            company_id = vac['employer']['id']
            title = vac['name']
            if 'salary' in vac and vac['salary'] is not None:
                salary_from = vac['salary'].get('from', 'Зарплата не указана')
                salary_to = vac['salary'].get('to', 'Зарплата не указана')
            else:
                salary_from = 'Зарплата не указана'
                salary_to = 'Зарплата не указана'
            link = vac['alternate_url']
            vacancy_data.append((vacancy_id, company_id, title, salary_from, salary_to, link))

        insert_query = (
            "INSERT INTO vacancies "
            "(vacancy_id, company_id, title, salary_from, salary_to, link) VALUES (%s, %s, %s, %s, %s, %s)")
        cur.executemany(insert_query, vacancy_data)

        conn.commit()
        print(f"Данные успешно добавлены в таблицы базы данных {Color.GREEN}{dbname}{Color.END}'!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Ошибка при добавлении данных:", error)
    finally:
        if conn is not None:
            conn.close()
