import requests
import json

url = 'https://clinicaltrials.gov/api/v2/studies'

# uses nctID to find specific trials

response = requests.get(url)
print(response)
response_dict = response.json()
# response_dict.dtype

print(json.dumps(response_dict, indent = 2, sort_keys = True))

# print(data)

print(response_dict.keys())
# print(response_dict['studies'][3]) # basic .json file

# url = f"https://clinicaltrials.gov/api/query/study_fields?expr=cancer"
# response = requests.get(url)
# print(response)

url =  "https://clinicaltrials.gov/api/v2/studies?format=json&query.cond=lung+cancer&query.locn=los+angeles&filter.overallStatus=ENROLLING_BY_INVITATION" 
overallStatus = """ENROLLING_BY_INVITATION"""
# need to let user input then run the query myself
# save the information somehow, with csv
# only want certain information, not all of it
response = requests.get(url)
print(response)