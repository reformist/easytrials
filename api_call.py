import requests
url = 'https://clinicaltrials.gov/api/v2/studies'

response = requests.get(url)
print(response)
response_dict = response.json()
print(response_dict.keys())
print(response_dict['studies'])