import pytest
from src.dbmanager_class.dbmanager import DBManager


@pytest.fixture(scope="module")
def db_manager():
    return DBManager(dbname="test_database")


def test_connect(db_manager):
    db_manager.connect(dbname="test_database")
    assert db_manager.conn is not None


def test_disconnect(db_manager):
    db_manager.connect(dbname="test_database")
    db_manager.disconnect()
    assert db_manager.conn is None


def test_close(db_manager):
    db_manager.connect(dbname="test_database")
    db_manager.close()
    assert db_manager.conn is None


def test_get_companies_and_vacancies_count(db_manager):
    db_manager.connect(dbname="test_database")
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    assert isinstance(companies_and_vacancies, list)


def test_get_all_vacancies(db_manager):
    db_manager.connect(dbname="test_database")
    all_vacancies = db_manager.get_all_vacancies()
    assert isinstance(all_vacancies, list)


def test_get_avg_salary(db_manager):
    db_manager.connect(dbname="test_database")
    avg_salary = db_manager.get_avg_salary()
    assert isinstance(avg_salary, float) or avg_salary is None


def test_get_vacancies_with_higher_salary(db_manager):
    db_manager.connect(dbname="test_database")
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    assert isinstance(higher_salary_vacancies, list)


def test_get_vacancies_with_keyword(db_manager):
    db_manager.connect(dbname="test_database")
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword("Python")
    assert isinstance(vacancies_with_keyword, list)
