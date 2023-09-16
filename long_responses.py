import random

# ask for two things: disease and location
# how to store information from patient

R_MY_LOCATION= "[need to make var to store this]"
R_STUDY_LOCATION = "[api call for five relevant studies]"
R_CONTACT = "[API call for contact of person running study]"
R_DISEASE = "[store for query]"

def unknown():
    response = ['Could you please re-phrase that?',
                "...",
                "Sounds about right",
                "What does that mean?"][random.randrange(4)]
    
    return response