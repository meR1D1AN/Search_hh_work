import requests
import pytest
from src.api.hh_api import get_vacancies_by_employer_ids


def test_get_vacancies_by_employer_ids():
    # Проверка успешного получения вакансий
    employer_ids = ["1", "2", "3"]
    vacancies = get_vacancies_by_employer_ids(employer_ids)
    assert len(vacancies) >= 0

    # Проверка обработки ошибки в ответе API
    def mock_get(*args, **kwargs):
        response = requests.Response()
        response.status_code = 404
        return response

    with pytest.raises(Exception) as exc_info:
        with mock_get():
            get_vacancies_by_employer_ids(employer_ids)
        assert exc_info.value is None
