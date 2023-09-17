from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd

import re
import long_responses as long
import finding_all_locations as location

import api_call_v2_mi as fdaAPI
import requests

import zipcodes

# NOT IMPORTANT
df2 = pd.read_csv(r"C:\Users\ndjed\Downloads\drug_trials_import\zip_codes.csv", sep = ';')
zipcode_list = df2.iloc[:,0].tolist()

for i in range(len(zipcode_list)):
    zipcode_list[i] = str(zipcode_list[i])



app = Flask(__name__)

CORS(app)

FDA_API_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
# I need to use Mi's code here

@app.route('/') # because I didn't say a http method, defaults to Get
def hello():

    res = jsonify('Hello, Flask!')
    # res.headers.add("Access-Control-Allow-Origin", "*")
    return res

def message_probability(user_message, recognized_words, single_response=False, required_words = []):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message: # depending if recognized words are in user message
        if word in recognized_words:
            message_certainty += 1
    
    percentage = float(message_certainty)/ float(len(recognized_words))

    # Check that the rqeuired words are in the string
    for word in required_words: # make sure we don't match to a wrong sentences
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        # print(percentage * 100)
        return percentage*100
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello! Please enter your location zip code in the format "Zipcode: XXXXX to find a trial near you.', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    # response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(long.R_MY_LOCATION, zipcode_list, required_words=["zipcode:"])
    # need to store responses somehow



    response(long.R_CONTACT, ['who', 'contact'], required_words = ['contact'])
    # response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}') 
    #dvp0



    return long.unknown() if highest_prob_list[best_match] < 0.000000001 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower()) # removes symbols from messages
    # print(patientZipcode)
    response = check_all_messages(split_message)
    # print(response) # returns None?
    return response

@app.route('/fda', methods = ['POST'])
def test_fda_api():

    data = request.get_json()

    split_message = re.split(r'\s+|[,;?!.-]\s*', data['message'].lower())
    for i in split_message:
            # print(i)
        if i == 'zipcode:':
            global zipCode
            zipCode = split_message[-1]
            print(zipCode)
    zipcode_info = zipcodes.matching(zipCode)[0]
    lat, long = zipcode_info["lat"], zipcode_info["long"]
    print("test")
    # zip_code = '10027'  # Replace with a valid ZIP code
        
    params = {
        "query.cond": "breast cancer",
        "pageSize": "1",
        'postFilter.geo': f'distance({lat},{long},50mi)'
    }
    try:
        response = requests.get(FDA_API_BASE_URL, params=params)
        if response.status_code == 200:
            clinical_trials_data = response.json()
            # I get a python object
            locationOfStudies = []
            for study in clinical_trials_data['studies']:
                protocolSection = study['protocolSection']
                locationOfStudies = protocolSection["contactsLocationsModule"]
                locationOfStudiesFirst = locationOfStudies['locations'][0]
                locationOfStudiesFirstFacility= locationOfStudiesFirst['facility']
                print(locationOfStudiesFirstFacility) # this is a list of of dictionaries of locations

            return (jsonify(locationOfStudiesFirstFacility)), 200
        else:
            return jsonify({'error': 'Failed to fetch clinical trials data.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['POST'])
def handle_post_request():
    try:
                # data = request.get_json()  # Retrieve JSON data from the request
        # user_message = data['message']
        data = request.get_json()  # Retrieve JSON data from the request
        # Process the data and generate a response
        split_message = re.split(r'\s+|[,;?!.-]\s*', data['message'].lower())
        for i in split_message:
            # print(i)
            if i == 'zipcode:':
                global zipCode
                zipCode = split_message[-1]
                print(zipCode)
                try:
                    params = {
                            'query.cond': "cancer",
                            'pageSize': "1",
                            # "max_rnk": 2,
                            # "min_rnk": 1,
                            # "max_rnk": 10,  # Adjust the number of results you want to retrieve
                            # "fmt": "json",
                        }
                    response = requests.get(FDA_API_BASE_URL, params=params)
                    print(response.status_code)
                    print('test')
                    if response.status_code == 200:
                        print("test2")
                        clinical_trials_data = response.json()
                        print("test3")
                        data_type = type(clinical_trials_data)
                        print(data_type)
                        print(clinical_trials_data)
                        response_data_test = "Data received successfully"
                        return jsonify(clinical_trials_data), 200
                    
                    else:
                        return jsonify({'error': 'Failed to fetch clinical trials data.'}), 400
                except Exception as e:
        
                    return jsonify({'error': str(e)}), 400
                        
                # fdaAPI.get("cancer", zipCode,50).to_json(response_data, orient="records", lines=True)
                # response_data= "test.json"
                print(zipCode)

            else:
                response_data = get_response("Bot: " + data['message'])

        # print(zipCode)
        # print(location.zipcode_list)

        

        # if re.match(r'^Zipcode: \d{5}$', user_message):
        #     user_zipcode = user_message.split(' ')[-1]  # Extract and store the zipcode
        #     response_data = f"Zipcode {user_zipcode} is saved. How can I assist you?"
        # else:
        #     response_data = get_response("Bot: " + user_message)
        response_data_test = {'message': 'Data received successfully'}
        return jsonify(response_data), 200  # Return a JSON response with a 200 status code
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Return an error response with a 400 status code
    



if __name__ == '__main__':
    app.run()