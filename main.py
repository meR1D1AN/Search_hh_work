from src.dbmanager_class.dbmanager import DBManager
from src.create_db.create_db import create_tables, create_database, fill_tables
from src.color.color import Color


def print_menu():
    """
    Печатает меню опций для взаимодействия с базой данных. Эта функция отображает меню опций пользователю для
    выполнения различных операций с базой данных.
    Эта функция не принимает параметров и ничего не возвращает.
    """
    print("\nВведите, что вы хотите сделать с базой данных:")
    print("\t1. Вывести компанию и количество вакансий")
    print("\t2. Вывести список всех вакансий")
    print("\t3. Вывести среднюю зарплату")
    print("\t4. Вывести вакансии с зарплатой выше среднего")
    print("\t5. Вывести вакансии в названии которых есть определенное слово")
    print("\t0. Выйти из программы")


def main():
    """
    Запускает программу, в которой пользователь может взаимодействовать с менеджером базы данных для
    выполнения различных операций. Эта функция подключается к менеджеру базы данных и представляет меню пользователю.
    Пользователь может выбрать один из следующих вариантов:
    1. Отобразить количество вакансий для каждой компании.
    2. Отобразить список всех вакансий вместе с их деталями.
    3. Вычислить и отобразить среднюю зарплату.
    4. Отобразить список вакансий с зарплатой выше среднего.
    5. Поиск вакансий по ключевому слову.
    0. Выход из программы.
    Функция непрерывно отображает меню и выполняет выбранную пользователем операцию на основе его выбора.
    После того, как пользователь выбирает выйти, функция отключается от менеджера базы данных.
    """
    dbname = input("Введите имя базы данных: ")
    # create_database(dbname)
    # create_tables(dbname)

    #  Выбраны 10 компаний
    fill_tables(dbname, ['3529', '78638', '80', '673', '8988088', '4181', '2748', '3776', '1740', '15478'])

    db_manager = DBManager(dbname=dbname)
    db_manager.connect(dbname=dbname)

    while True:
        print_menu()
        choice = input("Ваш выбор: ")

        if choice == "1":
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            print("\nКомпания - Количество вакансий:")
            for company, vacancies_count in companies_and_vacancies:
                print(f"{company}: {Color.U}{vacancies_count}{Color.U_} вакансий")

        elif choice == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for company, title, salary_from, salary_to, link in all_vacancies:
                if salary_from == "Зарплата не указана":
                    print(f"{company}: {title} - {Color.U}{salary_from}{Color.U_} - {link}")
                elif salary_to is None:
                    print(f"{company}: {title} - {Color.U}{salary_from}{Color.U_} - {link}")
                elif salary_from == "null":
                    print(f"{company}: {title} - {Color.U}{salary_to}{Color.U_} - {link}")
                else:
                    print(f"{company}: {title} - "
                          f"{Color.U}{salary_from}{Color.U_}-{Color.U}{salary_to}{Color.U_} - {link}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\nСредняя зарплата: {Color.U}{avg_salary}{Color.U_}")

        elif choice == "4":
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше среднего:")
            for company, title, salary_from, salary_to, link in high_salary_vacancies:
                if salary_to is None:
                    print(f"{company}: {title} - {Color.U}{salary_from}{Color.U_} - {link}")
                elif salary_from == "null":
                    print(f"{company}: {title} - {Color.U}{salary_to}{Color.U_} - {link}")
                else:
                    print(f"{company}: {title} - "
                          f"{Color.U}{salary_from}{Color.U_}-{Color.U}{salary_to}{Color.U_} - {link}")

        elif choice == "5":
            keyword = input("Введите слово для поиска: ")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nВакансии с названием, содержащим слово '{Color.GREEN}{keyword}{Color.END}':")
            for company, title, salary, link in vacancies_with_keyword:
                print(f"{company}: {title} - {Color.U}{salary}{Color.U_} - {link}")

        elif choice == "0":
            print(f"{Color.GREEN}Программа завершена.{Color.END}")
            break

        else:
            print(
                f"{Color.RED}Некорректный ввод. Пожалуйста, выберите опцию от "
                f"{Color.U}0{Color.U_} {Color.RED}до {Color.U}5{Color.U_}{Color.RED}.{Color.END}")

    db_manager.disconnect()


if __name__ == "__main__":
    main()
