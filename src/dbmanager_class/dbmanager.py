import psycopg2
import os
from src.color.color import Color
from typing import List, Tuple

pas_sql: str = os.environ['SQLPASS']


class DBManager:
    """
    Инициализирует DBManager с предоставленными параметрами.
    Параметры:
        dbname (str): Название базы данных. По умолчанию "kur_5".
        user (str): Имя пользователя для подключения к базе данных. По умолчанию "postgres".
        password (str): Пароль для соединения с базой данных.
        host (str): Адрес хоста базы данных. По умолчанию "localhost".
        port (str): Номер порта базы данных. По умолчанию "5432".
    """

    def __init__(self, dbname: str, user: str, password: str = pas_sql, host: str = "localhost",
                 port: str = "5432") -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self, dbname) -> None:
        """
        Подключается к базе данных PostgreSQL с использованием указанных параметров.
        Эта функция устанавливает соединение с базой данных PostgreSQL, используя указанное имя базы данных,
        имя пользователя, пароль, хост и порт. Если соединение успешно, то устанавливает атрибут `conn`
        в объект соединения и атрибут `cur` в объект курсора. Также выводит сообщение об успешном подключении.
        Если при попытке подключения возникает ошибка, выводит сообщение об ошибке с конкретным исключением.
        Параметры:
            self (DBManager): Экземпляр класса DBManager.
        Возвращает:
            None
        """
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print(f"Успешное подключение к базе данных {Color.GREEN}{dbname}{Color.END}!\n")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при подключении к базе данных:", error)

    def disconnect(self) -> None:
        """
        Отключается от базы данных, если соединение уже установлено.
        Параметры:
            self (объект): Экземпляр класса.
        Возвращает:
            None
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("\nОтключение от базы данных.")

    def close(self) -> None:
        """
        Закрывает соединение с базой данных, если оно открыто.
        Эта функция проверяет, не является ли атрибут `conn` текущего объекта не равным None. Если это так,
        то закрывает соединение с базой данных, вызывая метод `close()` для объекта `conn`. После закрытия
        соединения выводит сообщение "Соединение с базой данных закрыто.".
        Параметры:
            self (object): Текущий объект.
        Возвращает:
            None
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("Соединение с базой данных закрыто.")

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает имена компаний вместе с количеством вакансий, которые у них есть.
        """
        self.cur.execute(
            "SELECT c.name, COUNT(v.vacancy_id) AS vacancies_count FROM companies c "
            "JOIN vacancies v ON c.company_id = v.company_id GROUP BY c.name")
        companies_and_vacancies = self.cur.fetchall()
        return companies_and_vacancies

    def get_all_vacancies(self) -> List[Tuple[str, str, str, str]]:
        """
        Получает все вакансии из базы данных, включая название компании, название вакансии, зарплату и ссылку.
        Возвращает:
            list: Список кортежей, где каждый кортеж содержит название компании, название вакансии, зарплату и ссылку.
        """
        self.cur.execute(
            "SELECT c.name, v.title, v.salary_from, v.salary_to, v.link FROM companies c "
            "JOIN vacancies v ON c.company_id = v.company_id")
        all_vacancies = self.cur.fetchall()
        return all_vacancies

    def get_avg_salary(self) -> float:
        """
        Вычисляет среднюю зарплату из столбца 'salary_from' таблицы 'vacancies'.
        Возвращает:
            float: Средняя зарплата, округленная до 2 знаков после запятой.
        """
        query = """
                SELECT AVG(CASE WHEN salary_from = 'Зарплата не указана' 
                THEN NULL ELSE CAST(salary_from AS INTEGER) END) 
                FROM vacancies
                WHERE salary_from != 'Зарплата не указана'
                """
        self.cur.execute(query)
        avg_salary = self.cur.fetchone()[0]
        if avg_salary is not None:
            return round(avg_salary, 2)
        else:
            return None

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, str, str]]:
        """
        Извлекает вакансии с более высокой зарплатой.
        Возвращает:
            list: Список кортежей, где каждый кортеж содержит название компании, название вакансии, зарплату и ссылку.
        """
        self.cur.execute(
            "SELECT c.name, v.title, v.salary_from, v.salary_to, v.link "
            "FROM companies c JOIN vacancies v ON c.company_id = v.company_id "
            "WHERE CASE WHEN v.salary_from != 'Зарплата не указана' THEN CAST(v.salary_from AS INTEGER) ELSE 0 END > "
            "(SELECT AVG(CASE WHEN salary_from != 'Зарплата не указана' "
            "THEN CAST(salary_from AS INTEGER) ELSE NULL END) FROM vacancies)"
        )
        higher_salary_vacancies = self.cur.fetchall()
        return higher_salary_vacancies

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, str, str]]:
        """
        Получает вакансии с указанным ключевым словом из базы данных.
        Параметры:
            keyword (str): Ключевое слово для поиска в названиях вакансий.
        Возвращает:
            List[Tuple]: Список кортежей, содержащих название компании, название вакансии, начальную зарплату и
            ссылку на каждую вакансию, которая совпадает с ключевым словом.
        """
        self.cur.execute(
            f"SELECT c.name, v.title, v.salary_from, v.salary_to, v.link FROM companies c "
            f"JOIN vacancies v ON c.company_id = v.company_id WHERE v.title ILIKE %s",
            (f'%{keyword}%',))
        vacancies_with_keyword = self.cur.fetchall()
        return vacancies_with_keyword
