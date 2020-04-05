import urllib.request
import numpy
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# returns the dictionary of the state's data
def get_data_for_state(state):
    url_for_api ="https://covidtracking.com/api/states/daily?state=" + state
    with urllib.request.urlopen(url_for_api) as url:
        data = json.loads(url.read().decode())
    return data

def get_dict_of_state(state):
    data = get_data_for_state(state)

    positive_cases = []   # list of number of positive cases given a state
    positive_changes = [] # list of changes of positive cases 
    negative_cases = [] # list of number of negative changes
    negative_changes = [] # list of changes of negative cases
    total_tests = [] # number of tests administered
    total_changes = [] # change in tests given
    hospitalized = [] # number of people hospitalized
    hospitalized_changes = [] # change in number of people hospitalized
    death = [] # number of people dead from virus
    death_changes = [] # change in deaths

    # getting the data for each category and putting them in their own lists
    for obj in data:
        positive_cases.append(obj["positive"])
        positive_changes.append(obj["positiveIncrease"])
        negative_cases.append(obj["negative"])
        negative_changes.append(obj["negativeIncrease"])
        total_tests.append(obj["totalTestResults"])
        total_changes.append(obj["totalTestResultsIncrease"])
        hospitalized.append(obj["hospitalized"])
        hospitalized_changes.append(obj["hospitalizedIncrease"])
        death.append(obj["death"])
        death_changes.append(obj["deathIncrease"])
    
    # putting all the data into one dictionary for each state
    dict_for_state = {
        "positive cases": positive_cases,
        "positive changes": positive_changes,
        "negative cases": negative_cases,
        "negative changes": negative_changes,
        "total tests": total_tests,
        "total changes": total_changes,
        "hospitalized": hospitalized,
        "hospital changes": hospitalized_changes,
        "death cases": death,
        "death changes": death_changes
    }

    return dict_for_state

print(get_dict_of_state("WA"))
    
