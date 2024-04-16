import requests
from src.color.color import Color


def get_vacancies_by_employer_ids(employer_ids):
    """
    Получает вакансии по идентификаторам работодателей.
    Описание:
        Функция отправляет GET-запрос к API HH для получения вакансий по идентификаторам работодателей.
        Она итерируется по страницам ответа API и добавляет вакансии в список.
        Максимальное количество вакансий на одной странице и максимальное количество страниц с вакансиями задаются
        как константы.
        Если статус-код ответа API не равен 200, выводится сообщение об ошибке и цикл прерывается.
        Функция возвращает список полученных вакансий.
    """
    url = 'https://api.hh.ru/vacancies'
    all_vacancies = []

    page = 0
    per_page = 100  # Максимальное количество вакансий на одной странице
    max_page = 19  # Максимальное количество страниц с вакансиями, потом ошибка 400

    while page < max_page:
        params = {'employer_id': employer_ids, 'per_page': per_page, 'page': page}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            vacancies_on_page = data['items']
            all_vacancies.extend(vacancies_on_page)
            page += 1
        else:
            print(f'Ошибка при получении данных со страницы '
                  f'{Color.RED}{page}{Color.END}: {Color.RED}{response.status_code}{Color.END}')
            break

    return all_vacancies
