from hhapi import HHApi


hh_api = HHApi()

if __name__ == '__main__':
    employers = []
    companies = input('Введите через пробел список работодателей: ').split()
    for employer in companies:
        hh_api.get_employers_by_keyword(employer, employers)
    for employer in employers:
        print(employer)