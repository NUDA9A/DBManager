import requests


def get_salary(left, right, currency):
    """Формирует строку зарплаты"""
    if left is None and right is None:
        salary = None
    elif left is None and right is not None:
        salary = str(right) + " " + currency
    elif left is not None and right is None:
        salary = str(left) + " " + currency
    else:
        salary = str(left) + " - " + str(right) + " " + currency
    return salary


class HHApi:
    def __init__(self):
        self.url = 'https://api.hh.ru/'

    def get_employers_by_keyword(self, text: str, employers):
        """Получает список работодателей по запросу и заполняет ими массив employers"""
        params = {
            'text': text,
            'only_with_vacancies': True,
            'area': 113,
            'page': 0,
            'per_page': 100,
            'sort_by': 'by_vacancies_open'
        }

        req = requests.get(self.url + 'employers', params=params)

        if req.status_code == 200:
            data = req.json()
            if len(data['items']) == 1:
                employers.append([data['items'][0]['id'], data['items'][0]['name'], data['items'][0]['open_vacancies']])
                return
            elif len(data['items']) == 0:
                return
            employers.append([data['items'][0]['id'], data['items'][0]['name'], data['items'][0]['open_vacancies']])
            employers.append([data['items'][1]['id'], data['items'][1]['name'], data['items'][1]['open_vacancies']])
        else:
            print('Не удалось получить список работодателей.')

    def get_vacancies(self, employer_id):
        """Получает вакансии по id работодателя и возвращает список из словарей-вакансий"""
        params = {
            'employer_id': int(employer_id),
            'area': 113,
            'page': 0,
            'per_page': 100
        }
        req = requests.get(self.url + 'vacancies', params=params)
        data = req.json()
        vacancies = []
        for vacancy in data['items']:
            if vacancy.get('salary'):
                salary = get_salary(vacancy['salary']['from'], vacancy['salary']['to'], vacancy['salary']['currency'])
            else:
                salary = None
            curr_vacancy = {
                'name': vacancy['name'],
                'employer_id': int(employer_id),
                'salary': salary,
                'url': vacancy['alternate_url']
            }
            vacancies.append(curr_vacancy)
        return vacancies
