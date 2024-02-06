import requests


class HHApi:
    def __init__(self):
        self.url = 'https://api.hh.ru/'

    def get_employers_by_keyword(self, text: str, employers):
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