import requests
import json

url = 'https://clinicaltrials.gov/api/v2/studies'

params = {
    'format' : 'json',
    'query.cond': 'lung+cancer',
    'query.locn' : 'los+angeles',
    'filter.overallStatus': 'ENROLLING_BY_INVITATION',
}

# location = input("Please enter your location: ")
# location = location.lower().replace(" ", "+")

# print(location)

response = requests.get(url, params = params)

#first dict call is ['studies']
# then the next call can be either ['protocolSection', 'derivedSection', or 'hasResults']
if response.status_code == 200:
    data = response.json()
    print(data.keys())
    # print(data["studies"]) #
    # Iterate through the studies in the response
    count = 0
    for study in data['studies']:
        protocolSection = study['protocolSection']
        locationOfStudies = protocolSection["contactsLocationsModule"]
        print(locationOfStudies['locations'][0]) # this is a list of of dictionaries of locations
        

        # print(study).head()
        # count += 1
        # if count >= 1:
        #     break
        # Access specific information about each study
        # print(f"Title: {study['brief_title']}")
        # print(f"NCT ID: {study['nct_id']}")
        # print(f"Overall Status: {study['overall_status']}")
        # print("\n")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
# uses nctID to find specific trials

# response = requests.get(url)
# # print(response)
# response_dict = response.json()

# with open(response_dict, 'r') as json_file:
#     data = json.load(response_dict)
#     for item in data:
#         print(item)
# # response_dict.dtype

# # print(json.dumps(response_dict, indent = 2, sort_keys = True))

# # print(data)

# # print(response_dict.keys())
# # print(response_dict['studies'][3]) # basic .json file

# # url = f"https://clinicaltrials.gov/api/query/study_fields?expr=cancer"
# # response = requests.get(url)
# # print(response)
# overallStatus = """ENROLLING_BY_INVITATION"""
# search_terms = """autism+OR+autism+spectrum+disorder+OR+Fragile+X+OR+Rett+syndrome+OR+tuberous+sclerosis+OR+Williams+syndrome+OR+
#                 Praeder+Willi+syndrome+OR+Phelan+McDermid+syndrome+OR+Dup15q+OR+Angelman+OR+Timothy+syndrome+OR+16p+deletion+OR+16p+duplication+OR+ADNP"""

# url =  f"https://clinicaltrials.gov/api/v2/studies?format=json&query.cond=lung+cancer&query.locn=los+angeles&filter.overallStatus={overallStatus}" 
# # need to let user input then run the query myself
# # save the information somehow, with csv
# # only want certain information, not all of it
# response = requests.get(url)
# with open(response.json(), 'r') as json_file:
#     data = json.load(response_dict)
#     for item in data:
#         print(item)