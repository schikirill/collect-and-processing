import requests
import json

username = input('Enter username: \n') #  например, schikirill
response = requests.get(f'https://api.github.com/users/{username}/repos')

repos_list = {f'{username} repositories': []}

with open('user_repos.json', 'w') as f:
    for repo in response.json():
        repos_list[f'{username} repositories'].append({'name': repo['name']})
    json.dump(repos_list, f)

print(repos_list)

