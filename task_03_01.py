from bs4 import BeautifulSoup as bs
import pymongo
from pymongo import MongoClient
import requests
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_shop']
vacancys = db['vacancys']


# def vacancies_from_db_get():
#     client = MongoClient('127.0.0.1', 27017)
#     db = client['vacancy_shop']
#     vacancys = db['vacancys']
#     urls = vacancys.distinct('link')
#     client.close()
#     return urls


def vacancies_to_db_save(args):
    num = 0
    for element in vakancy_lists:
        if not vacancys.find_one({'link': element['link']}):
            vacancys.insert_one(element)
            num += 1

    print(f'Added {num} vacancies')


def vacancies_salary_find(bucks):
    money = []
    for element in vacancys.find({'$or': [{'salary.from': {'$gt': bucks}}, {'salary.to': {'$gt': bucks}}]}):
        money.append(element)
    print(f'\nFound {len(money)} vacancies\n')
    return money


def work_finding():
    job = input("Looking for job: ")

    while True:
        money = input("Only with salary (y/n)? ")
        if money.lower() == 'y':
            money = 'true'
            break
        elif money.lower() == 'n':
            money = 'false'
            break
        else:
            print("Only y or n accepted! Try again/")

    while 1:
        try:
            pages = int(input("Pages: "))
            break
        except ValueError:
            print("Number needed")

    main_url = 'https://rabota.by/search/vacancy'
    vakancy_lists = []

    page = 0

    while page < pages:
        params = {'text': job,
                  'page': page,
                  'only_with_salary': money
                  }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.3.927 Yowser/2.5 Safari/537.36'}
        response = requests.get(main_url, params=params, headers=headers)
        if response.ok:
            dom = bs(response.text, 'html.parser')
            jobs = dom.find_all('div', {'class': 'vacancy-serp-item'})
            for vakancy in jobs:
                job_data = {}
                salary_dict = {}
                name = vakancy.find('a', {'class': 'bloko-link'}).text
                city = vakancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.replace('\xa02\xa0', '')
                link = vakancy.find('a', {'class': 'bloko-link'}).get('href')
                try:
                    salary = vakancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}) \
                        .text.replace('\u202f', '').replace('\xa0', '').split()
                    if len(salary) == 3:
                        if salary[0] == "от":
                            salary_dict = dict({('from', int(salary[1])), ('to', "None"), ('currency', salary[2])})
                        elif salary[0] == "до":
                            salary_dict = dict({('from', "None"), ('to', int(salary[1])), ('currency', salary[2])})
                    elif len(salary) == 4:
                        salary_dict = dict({('from', int(salary[0])), ('to', int(salary[2])), ('currency', salary[3])})
                except:
                    salary_dict = dict({('from', "None"), ('to', "None"), ('currency', "None")})

                job_data['name'] = name
                job_data['city'] = city
                job_data['link'] = link
                job_data['salary'] = salary_dict

                vakancy_lists.append(job_data)

        page += 1

    return vakancy_lists


vakancy_lists = work_finding()

vacancies_to_db_save(vakancy_lists)

bucks = int(input("Minimum salary?: "))
good_vacacy = vacancies_salary_find(bucks)
pprint(good_vacacy)

client.close()
