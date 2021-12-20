from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

# https://rabota.by/search/vacancy?search_field=name&search_field=company_name&search_field=description&only_with_salary=true&clusters=true&ored_clusters=true&enable_snippets=true&text=Data+science
# job = "слесарь"
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
    headers = {'User-Agent': 'Boo!!!'}
    response = requests.get(main_url, params=params, headers=headers)
    if response.ok:
        dom = bs(response.text, 'html.parser')
        jobs = dom.find_all('div', {'class': 'vacancy-serp-item'})
        for vakancy in jobs:
            job_data = {}
            salary_dict = {}
            name = vakancy.find('a', {'class': 'bloko-link'}).text
            link = vakancy.find('a', {'class': 'bloko-link'}).get('href')
            try:
                salary = vakancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}) \
                        .text.replace('\u202f', '').replace('\xa0', '').split()
                if len(salary) == 3:
                    if salary[0] == "от":
                        salary_dict = dict({('from', salary[1]), ('currency', salary[2])})
                    elif salary[0] == "до":
                        salary_dict = dict({('to', salary[1]), ('currency', salary[2])})
                elif len(salary) == 4:
                    salary_dict = dict({('from', salary[0]), ('to', salary[2]), ('currency', salary[3])})
            except:
                salary_dict = dict({('min', ''), ('max', "Unpaid work"), ('currency', '')})

            job_data['name'] = name
            job_data['link'] = link
            job_data['salary'] = salary_dict

            vakancy_lists.append(job_data)

    page += 1
pprint(vakancy_lists)
