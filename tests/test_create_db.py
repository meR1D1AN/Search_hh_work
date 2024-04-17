import psycopg2
import pytest
from src.create_db.create_db import create_database, create_tables, fill_tables
from src.color.color import Color


@pytest.fixture(scope="module")
def dbname():
    return "test_database"


def check_database_exists(dbname):
    """Проверяет наличие базы данных."""
    try:
        conn = psycopg2.connect(dbname=dbname)
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False


def test_create_database(dbname, capsys):
    if not check_database_exists(dbname):
        create_database(dbname)
    else:
        print(f"База данных {Color.RED}{dbname}{Color.END} уже существует!")

    captured = capsys.readouterr()
    assert f"База данных {Color.RED}{dbname}{Color.END} уже существует!" in captured.out


def test_create_tables(dbname, capsys):
    create_tables(dbname)
    captured = capsys.readouterr()
    assert f"Таблицы успешно созданы в базе данных \033[92m{dbname}\033[0m!" in captured.out


def test_fill_tables(dbname, capsys):
    employer_ids = ["12345", "67890"]  # Mock employer_ids for testing
    fill_tables(dbname, employer_ids)
    captured = capsys.readouterr()
    assert f"Данные успешно добавлены в таблицы базы данных \033[92m{dbname}\033[0m!" in captured.out
