from hhapi import HHApi
from db_manager import DBManager

hh_api = HHApi()
db_manager = DBManager()

if __name__ == '__main__':
    employers = []

    companies = input('Введите через пробел список работодателей: ').split()

    for employer in companies:
        hh_api.get_employers_by_keyword(employer, employers)

    """Заполняем таблицы данными"""
    # db_manager.fill_employers(employers)
    # db_manager.fill_vacancies(employers)

    """Пример работы функций"""

    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()

    print("Несколько работодателей и кол-во их вакансий:")

    for i in range(5):
        print(f"employer_id: {companies_and_vacancies_count[i][0]}, name: {companies_and_vacancies_count[i][1]}, кол-во вакансий: {companies_and_vacancies_count[i][2]}")
    print()

    all_vacancies = db_manager.get_all_vacancies()

    print("Несколько вакансий:")

    for i in range(5):
        salary = all_vacancies[i][2]
        if all_vacancies[i][2] is None:
            salary = 'Не указано'
        print(f"Работодатель: {all_vacancies[i][0]}, Вакансия: {all_vacancies[i][1]}, Зарплата: {salary}, url: {all_vacancies[i][3]}")
    print()

    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата: {avg_salary}")

    print()

    print("Пример вывода вакансий с зарплатой выше средней:")

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()

    for i in range(5):
        print(f"Вакансия: {vacancies_with_higher_salary[i][0]}, Зарплата: {vacancies_with_higher_salary[i][1]}, url: {vacancies_with_higher_salary[i][2]}")

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
