# Проект "Управление вакансиями"

Этот проект представляет собой программу для управления базой данных вакансий с использованием API HeadHunter.

## Запуск проекта

1. Склонируйте репозиторий на локальный компьютер:

   `git clone https://github.com/meR1D1AN/search_hh_work`

2. Установите зависимости, выполнив команду:

   `pip install -r requirements.txt`

3. Создайте файл окружения `.env` в корневом каталоге проекта и укажите в нем свои настройки, включая пароль к базе
   данных:

   `SQLPASS=your_password_here`
4. Запустите программу, выполнив команду:

   `python main.py`

## Использование программы

После запуска программы вы увидите меню опций, которые вы можете выбрать:

1. Вывести компанию и количество вакансий.
2. Вывести список всех вакансий.
3. Вычислить и отобразить среднюю зарплату.
4. Вывести список вакансий с зарплатой выше среднего.
5. Поиск вакансий по ключевому слову.
0. Выйти из программы.

Выберите нужную опцию, следуя инструкциям.

## Описание файлов

- `src/api/hh_api.py`: Модуль для работы с API HeadHunter.
- `src/create_db/create_db.py`: Модуль для создания базы данных и таблиц.
- `src/color/color.py`: Модуль для изменения цвета текста и подчёркивания в консоли.
- `src/dbmanager_class/dbmanager.py`: Модуль для работы с базой данных.
- `main.py`: Основной модуль программы.




