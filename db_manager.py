import psycopg2
from hhapi import HHApi


class DBManager:
    def __init__(self):
        self.hh_api = HHApi()

    def fill_employers(self, employers):
        """Заполняет таблицу employers"""
        conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()

        for employer in employers:
            curr.execute("INSERT INTO employers VALUES (%s, %s, %s)", (int(employer[0]), employer[1], employer[2]))

        conn.commit()
        curr.close()
        conn.close()

    def fill_vacancies(self, employers):
        """Заполняет таблицу vacancies"""
        conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()
        i = 1
        for employer in employers:
            vacancies = self.hh_api.get_vacancies(employer[0])
            for vacancy in vacancies:
                curr.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)", (i, vacancy['name'],
                                                                                   vacancy['employer_id'],
                                                                                   vacancy['salary'],
                                                                                   vacancy['url']))
                i += 1
        conn.commit()
        curr.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список компаний и кол-во их вакансий"""
        conn = conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()

        curr.execute("SELECT * FROM employers")

        rows = curr.fetchall()
        curr.close()
        conn.close()
        return rows

    def get_all_vacancies(self):
        """Получает список состоящий из имени работодателя, имени вакансии, зарплаты и ссылки на вакансию"""
        conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()

        curr.execute("SELECT DISTINCT employers.employer_name, vacancy_name, salary, vacancy_url\
                        FROM vacancies\
                        JOIN employers USING(employer_id)")

        rows = curr.fetchall()
        curr.close()
        conn.close()
        return rows

    def get_avg_salary(self):
        """Получает среднюю зарплату (вакансии, где зарплата не указана, не учитываются)"""
        conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()

        curr.execute("SELECT salary FROM vacancies")
        rows = curr.fetchall()
        curr.close()
        conn.close()

        s_salary = 0
        count = 0
        for row in rows:
            if row[0] is None:
                continue
            sal = row[0].split()
            if len(sal) == 2:
                s_salary += int(sal[0])
            else:
                s_salary += ((int(sal[0]) + int(sal[2])) / 2)
            count += 1
        avg_salary = (s_salary / count).__round__(2)
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """Получает вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()

        curr.execute("SELECT DISTINCT vacancy_name, salary, vacancy_url FROM vacancies")
        rows = curr.fetchall()
        curr.close()
        conn.close()

        result = []

        for row in rows:
            if row[1] is None:
                continue
            if len(row[1].split()) == 2:
                if int(row[1].split()[0]) >= avg_salary:
                    result.append(row)
            else:
                if (int(row[1].split()[0]) + int(row[1].split()[2])) / 2 >= avg_salary:
                    result.append(row)

        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий в названии которых есть переданное слово keyword"""

        result = []

        conn = psycopg2.connect(
            host='localhost',
            database='hh_vacancies',
            user='postgres',
            password='3525'
        )

        curr = conn.cursor()

        curr.execute("SELECT DISTINCT vacancy_name, salary, vacancy_url FROM vacancies")

        rows = curr.fetchall()
        curr.close()
        conn.close()
        for row in rows:
            if keyword in row[0]:
                result.append(row)
        return result
