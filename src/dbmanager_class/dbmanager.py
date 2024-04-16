import psycopg2
import os

pas_sql = os.environ['SQLPASS']


class DBManager:
    def __init__(self, dbname="kur_5", user="postgres", password=pas_sql, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print("Успешное подключение к базе данных!\n")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при подключении к базе данных:", error)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("\nDisconnected from database.")

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print("Соединение с базой данных закрыто.")

    def get_companies_and_vacancies_count(self):
        self.cur.execute(
            "SELECT c.name, COUNT(v.vacancy_id) AS vacancies_count FROM companies c "
            "JOIN vacancies v ON c.company_id = v.company_id GROUP BY c.name")
        companies_and_vacancies = self.cur.fetchall()
        return companies_and_vacancies

    def get_all_vacancies(self):
        self.cur.execute(
            "SELECT c.name, v.title, v.salary_from, v.link FROM companies c "
            "JOIN vacancies v ON c.company_id = v.company_id")
        all_vacancies = self.cur.fetchall()
        return all_vacancies

    def get_avg_salary(self):
        query = """
                SELECT AVG(CASE WHEN salary_from = 'Зарплата не указана' THEN NULL ELSE CAST(salary_from AS INTEGER) END)
                FROM vacancies
                WHERE salary_from != 'Зарплата не указана'
                """
        self.cur.execute(query)
        avg_salary = self.cur.fetchone()[0]
        return round(avg_salary, 2)

    def get_vacancies_with_higher_salary(self):
        self.cur.execute(
            "SELECT c.name, v.title, v.salary_from, v.link "
            "FROM companies c JOIN vacancies v ON c.company_id = v.company_id "
            "WHERE CASE WHEN v.salary_from != 'Зарплата не указана' THEN CAST(v.salary_from AS INTEGER) ELSE 0 END > "
            "(SELECT AVG(CASE WHEN salary_from != 'Зарплата не указана' "
            "THEN CAST(salary_from AS INTEGER) ELSE NULL END) FROM vacancies)"
        )
        higher_salary_vacancies = self.cur.fetchall()
        return higher_salary_vacancies

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute(
            f"SELECT c.name, v.title, v.salary_from, v.link FROM companies c "
            f"JOIN vacancies v ON c.company_id = v.company_id WHERE v.title ILIKE %s",
            (f'%{keyword}%',))
        vacancies_with_keyword = self.cur.fetchall()
        return vacancies_with_keyword


if __name__ == "__main__":
    db_manager = DBManager(dbname="kur_5", user="postgres", password=pas_sql, host="localhost", port="5432")
    db_manager.connect()

    # print("Компании и кол-во вакансий:")
    # companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    # for company, vacancies_count in companies_and_vacancies:
    #     print(f'{company}: {vacancies_count} вакансий')

    # print("\nСписок всех вакансий:")
    # all_vacancy = db_manager.get_all_vacancies()
    # for company, title, salary, link in all_vacancy:
    #     print(f'{company}: {title} - {salary} - {link}')

    # print("\nСредняя зарплата:")
    # print(db_manager.get_avg_salary())

    # print("\nВакансии с зарплатой выше среднего:")
    # high_avg = db_manager.get_vacancies_with_higher_salary()
    # for company, title, salary, link in high_avg:
    #     print(f'{company}: {title} - {salary} - {link}')

    # print("\nВакансии в названии которых есть слово 'python':")
    # vacancies_with_keyword = db_manager.get_vacancies_with_keyword("python")
    # for company, title, salary, link in vacancies_with_keyword:
    #     print(f'{company}: {title} - {salary} - {link}')
    db_manager.disconnect()
