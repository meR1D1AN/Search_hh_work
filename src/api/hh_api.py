import requests

API_TOKEN = 'your_api_token'
BASE_URL = 'https://api.hh.ru/vacancies'


def get_companies_and_vacancies():
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }

    params = {
        'area': 'moscow',
        'only_with_salary': True
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    companies = data['items']
    vacancies = data['found']

    return companies, vacancies


companies, vacancies_count = get_companies_and_vacancies()
print(f'Найдено {len(companies)} компаний и {vacancies_count} вакансий.')
