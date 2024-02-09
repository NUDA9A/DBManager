from hhapi import HHApi
from db_manager import DBManager


def user_interaction():
    command = ''
    while command != 5:
        print("Введите номер какой нибудь команды:\n"
              "1. Employers - Работодатели и кол-во их вакансий\n"
              "2. Vacancies - Список вакансий\n"
              "3. Salary - Средняя зарплата\n"
              "4. Vacancies with higher salary - Список вакансий с зарплатой выше средней\n"
              "5. Vacancies with keyword - Список вакансий с ключевым словом в названии вакансии\n"
              "6. Exit - Выход из работы программы")
        command = int(input()) - 1
        if command == 0:
            result = db_manager.get_companies_and_vacancies_count()
            print('Работодатели и кол-во их вакансий:')
            for employer in result:
                print(f"employer_id: {employer[0]}, name: {employer[1]}, кол-во вакансий: {employer[2]}")
            print()
        elif command == 1:
            result = db_manager.get_all_vacancies()
            print('Список вакансий:')
            for vacancy in result:
                salary = vacancy[2]
                if vacancy[2] is None:
                    salary = 'Не указано'
                print(f"Работодатель: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {salary}, url: {vacancy[3]}")
            print()
        elif command == 2:
            result = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {result}")
            print()
        elif command == 3:
            result = db_manager.get_vacancies_with_higher_salary()
            print("Список вакансий с зарплатой выше средней:")
            for vacancy in result:
                print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, url: {vacancy[2]}")
            print()
        elif command == 4:
            keyword = input("Введите ключевое слово для поиска: ")
            result = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in result:
                salary = vacancy[1]
                if vacancy[1] is None:
                    salary = 'Не указано'
                print(f"Вакансия: {vacancy[0]}, Зарплата: {salary}, url: {vacancy[2]}")
            print()
        elif command not in range(6):
            print("Неизвестная команда, попробуйте еще раз.")


hh_api = HHApi()
db_manager = DBManager()

if __name__ == '__main__':
    employers = []

    companies = input('Введите через пробел список работодателей: ').split()

    for employer in companies:
        hh_api.get_employers_by_keyword(employer, employers)

    """Создаем таблицы если они не созданы"""
    db_manager.create_tables()

    """Заполняем таблицы данными"""
    db_manager.fill_employers(employers)
    db_manager.fill_vacancies(employers)

    """Пример работы функций"""

    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()

    print("Несколько работодателей и кол-во их вакансий:")

    for i in range(5):
        print(
            f"employer_id: {companies_and_vacancies_count[i][0]}, name: {companies_and_vacancies_count[i][1]}, кол-во вакансий: {companies_and_vacancies_count[i][2]}")
    print()

    all_vacancies = db_manager.get_all_vacancies()

    print("Несколько вакансий:")

    for i in range(5):
        salary = all_vacancies[i][2]
        if all_vacancies[i][2] is None:
            salary = 'Не указано'
        print(
            f"Работодатель: {all_vacancies[i][0]}, Вакансия: {all_vacancies[i][1]}, Зарплата: {salary}, url: {all_vacancies[i][3]}")
    print()

    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата: {avg_salary}")

    print()

    print("Пример вывода вакансий с зарплатой выше средней:")

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()

    for i in range(5):
        print(
            f"Вакансия: {vacancies_with_higher_salary[i][0]}, Зарплата: {vacancies_with_higher_salary[i][1]}, url: {vacancies_with_higher_salary[i][2]}")

    print()

    print("Пример вывода вакансий с ключевым словом в названии:")

    vacancies_with_keyword = db_manager.get_vacancies_with_keyword('разработчик')

    for i in range(5):
        if vacancies_with_keyword[i][1] is None:
            salary = 'Не указано'
        if vacancies_with_keyword[i][1] is not None and len(vacancies_with_keyword[i][1].split()) == 2:
            salary = vacancies_with_keyword[i][1].split()[0]
        elif vacancies_with_keyword[i][1] is not None:
            salary = (int(vacancies_with_keyword[i][1].split()[0]) + int(vacancies_with_keyword[i][1].split()[2])) / 2
        print(f"Вакансия: {vacancies_with_keyword[i][0]}, Зарплата: {salary}, url: {vacancies_with_keyword[i][2]}")

    user_interaction()
    db_manager.close()
