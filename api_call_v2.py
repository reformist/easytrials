import requests
import pandas as pd
from io import StringIO
import re
import numpy as np
import zipcodes
import math
from geopy.distance import geodesic
import datetime
import matplotlib.pyplot as plt

#defaults
condition = "breast cancer"
target_zip = "10027" #remember to clip to 5 digits
max_distance = "50" #miles
num_out = -1
pagesize=20


def get(condition, zipcode, max_distance, pagesize=pagesize, sex="ALL", age="CHILD,ADULT,OLDER_ADULT"):
    """
    making the api call
    condition, zipcode, and max distance are strings
    pagesize can to up to 1000, but it get slow
    sex can be "ALL", "FEMALE", or "MALE"
    age can be "CHILD", "ADULT", or "OLDER_ADULT"
    """
    zipcode_info = zipcodes.matching(zipcode)[0]
    lat, long = zipcode_info["lat"], zipcode_info["long"]
    headers = {
    'accept': 'application/json',
    }
    params = {
        'format': 'csv',
        'filter.overallStatus': 'NOT_YET_RECRUITING,RECRUITING',
        'query.cond': condition,
        'postFilter.geo': f'distance({lat},{long},{max_distance}mi)',
        # 'Sex'
        'sort': '@relevance',
        'pageSize': str(pagesize),
        'fields': 'NCT Number,Study Title,Study URL,Study Status,Brief Summary,Study Results,Conditions,Interventions,Sex,Age,Phases,Enrollment,Start Date,Primary Completion Date,Locations'}
    response = requests.get('https://clinicaltrials.gov/api/v2/studies', params=params, headers=headers)
    csv_content = response.content.decode('utf-8')
    return pd.read_csv(StringIO(csv_content))


def parse_locations(df):
    """
    spliting location information from api call
    making a dataframe with NCT Number and each parsed location
    """
    #making the dictionary to make a dataframe later
    wanted_cols = ["NCT Number", "Place", "City", "State", "Zipcode", "Country"]
    out = {col: [] for col in wanted_cols}
    
    #iterate through the rows
    for i, row in df.iterrows():
        #splitting all the locations, then split each location into its parts
        splitted_locs = [loc.split(",") for loc in row["Locations"].split("|")]
        
        #iterate through each location
        for loc in splitted_locs:
            loc = [item.strip(" ") for item in loc]
            
            #only look in America
            if loc[-1] != "United States":
                continue

            #handling weird cases
            if len(loc) == 3:
                #only have state, zipcode, and country
                loc = [None] + loc[0:2] + [None] + [loc[-1]]
            elif len(loc) == 4:
                #missing zipcode
                loc = loc[:-1] + [None] + loc[-1:]
            elif len(loc) == 6:
                #accidentally split name of place when setting delimiter to ,
                loc[0] = loc[0] + ", " + loc.pop(1)
                #API repeat city and state
            elif len(loc) == 7:
                loc = loc[0:1] + loc[3:]
            elif len(loc) == 8:
                #when given street
                loc = ["".join(loc[:2])] + loc[4:]

            assert len(loc) == 5, f"len loc is not five {loc}"

            for col, new_thing in zip(wanted_cols, [row["NCT Number"]] + loc):
                out[col].append(new_thing)


    out = pd.DataFrame(out)
    return out[out['Zipcode'].notna()]

    

allowed_characters_pattern = re.compile(r'1234567890-')
def filter_zipcodes_within_radius(df, target_zip, radius_miles):
    tarparse_locationsation = zipcodes.matching(target_zip)
    if not tarparse_locationsation:
        print(f"ZIP code {target_zip} not found.")
        return pd.DataFrame()

    target_lat = tarparse_locationsation[0]['lat']
    target_lon = tarparse_locationsation[0]['long']

    def calculate_distance(row):
        row_zip = row['Zipcode']
        if len(row_zip) not in (5, 10) and not bool(allowed_characters_pattern.match(row_zip)):
            return None
        row_location = zipcodes.matching(row_zip)
        if not row_location:
            return None
        # print('hi!!')
        row_lat = row_location[0]['lat']
        row_lon = row_location[0]['long']

        distance = geodesic((target_lat, target_lon), (row_lat, row_lon)).miles
        return distance

    df['Distance'] = df.apply(calculate_distance, axis=1)

    filtered_df = df[df['Distance'] <= int(radius_miles)].copy()
    return filtered_df


def splitting(x):
    if not pd.isna(x):
        return x.split("|")
    return x

def sex_filter(user_sex, wanted_sex):
    if wanted_sex == "ALL":
        return True
    return user_sex == wanted_sex

def age_filter(user_age, wanted_age):
    return True
    user_age = int(user_age)
    if user_age <= 18:
        return "CHILD" in wanted_age
    elif user_age <= 64:
        return "ADULT" in wanted_age
    else:
        return "OLDER_ADULT" in wanted_age





def modified_sigmoid(x, c=10):
    '''
    take an int, return a float
    scaling distance x s.t. x >= 0 --> [0, 1], monotonically decreasing
    c is a constant to adjust for how sensitive a person is to distance/time from trial recruitment
    a larger c indicates less sensistivity and vice versa
    roughly speaking, c indicate the number of x such that f(x) ~= 1/2
    monotomically decreasing on all reals; range from 0 to 1
    we could set c=max_distance/2
    '''
    return -2 / (1+np.exp(-x/c)) + 2

def date_scale(x, c=365):
    '''
    take a Timestamp instant, return a float
    given a start date, return modified sigmoid step function
    x before/on current day --> 1
    x after current day --> modded sigmoid function
    '''
    until_trial = (x - pd.Timestamp(datetime.date.today())).days

    if until_trial <= 0:
        return 1
    
    return modified_sigmoid(until_trial, c=c)

def get_score(row, dist_weight=1, date_weight=1):
    return dist_weight*modified_sigmoid(row["Distance"]) + date_weight*date_scale(row["Start Date"])
    
    
def trial_api_call(condition=condition, zipcode=target_zip, max_distance=max_distance, num_out=num_out, pagesize=pagesize, user_age=18, user_sex="ALL"):
    """
    over arching function that call other functions
    given the above parameters, return top num_out clinical trials
    """
    #type casting for later functions
    max_distance, zipcode = str(max_distance), str(zipcode)
    #doing the actual api call
    df = get(condition, zipcode, max_distance, pagesize=pagesize)
    df = df[df['Age'].apply(lambda age: age_filter(user_age, age)) & df['Sex'].apply(lambda sex: sex_filter(user_sex, sex))]
    #cleaning up the data frame
    #spliltting age
    df["Age"] = df["Age"].apply(lambda x: x.split(", "))
    #splitting by |
    for col in ("Conditions", "Interventions"):#, "Other IDs", \
                # "Primary Outcome Measures", "Secondary Outcome Measures",\
                # "Other Outcome Measures", "Study Design"):
        df[col] = df[col].apply(splitting)

    #type cast into datetime
    for col in ("Start Date", "Primary Completion Date"): #,\
                # "Completion Date", "First Posted", \
                # "Results First Posted", "Last Update Posted"):
        df[col] = pd.to_datetime(df[col])

    #parse the location into a separate df
    loc_df = parse_locations(df)
    #filter the location to be within target radius
    filtered_loc_df = filter_zipcodes_within_radius(loc_df, zipcode, max_distance)
    #merged back to original df but only the locations that we want
    df = filtered_loc_df.merge(df, how="left", on="NCT Number", )
    #sorting to get closest locations
    df["Score"] = df.apply(get_score, axis=1)
    df.sort_values("Score", ascending=False, inplace=True)

    #temp output, to be better with a score model
    return df.iloc[:num_out, :]

#picking out conditions
df = trial_api_call()
conditions = {}
for i, row in df.iterrows():
    for condition in row["Conditions"]:
        conditions[condition] = conditions.get(condition, 0) + 1

conditions_df = pd.DataFrame({"Condition": [k for k in conditions.keys()],
                            "Occurence": [v for v in conditions.values()]})
    
conditions_df.sort_values("Occurence", ascending=False)


#plot modified_sigmoid/distance scale
# x = np.linspace(-25, 25, 500)
# y = modified_sigmoid(x)
# plt.figure(figsize=(10, 6))
# plt.plot(x, y, label='Modified Sigmoid Function', color='blue')
# plt.xlabel('Days from Start Date')
# plt.ylabel('Output')
# plt.title('Modified Sigmoid Function')
# plt.legend()
# plt.grid(True)
# plt.show()

# startdate = df["Start Date"][0]
# print(date_scale(startdate + datetime.timedelta(1)))