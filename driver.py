from getdata import *
from sir import *
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from plot import *
import time

# this the driver class where all the code will be run from
# getting the inital data from the github repo
covid_data = getDataFromUS()
state_map = [
    ["AL", "Alabama"],
    ["AK", "Alaska"],
    ["AZ", "Arizona"],
    ["AR", "Arkansas"],
    ["CA", "California"],
    ["CO", "Colorado"],
    ["CT", "Connecticut"],
    ["DE", "Delaware"],
    ["FL", "Florida"],
    ["GA", "Georgia"],
    ["HI", "Hawaii"],
    ["ID", "Idaho"],
    ["IL", "Illinois"],
    ["IN", "Indiana"],
    ["IA", "Iowa"],
    ["KS", "Kansas"],
    ["KY", "Kentucky"],
    ["LA", "Louisiana"],
    ["ME", "Maine"],
    ["MD", "Maryland"],
    ["MA", "Massachusetts"],
    ["MI", "Michigan"],
    ["MN", "Minnesota"],
    ["MS", "Mississippi"],
    ["MO", "Missouri"],
    ["MT", "Montana"],
    ["NE", "Nebraska"],
    ["NV", "Nevada"],
    ["NH", "New Hampshire"],
    ["NJ", "New Jersey"],
    ["NM", "New Mexico"],
    ["NY", "New York"],
    ["NC", "North Carolina"],
    ["ND", "North Dakota"],
    ["OH", "Ohio"],
    ["OK", "Oklahoma"],
    ["OR", "Oregon"],
    ["PA", "Pennsylvania"],
    ["RI", "Rhode Island"],
    ["SC", "South Carolina"],
    ["SD", "South Dakota"],
    ["TN", "Tennessee"],
    ["TX", "Texas"],
    ["UT", "Utah"],
    ["VT", "Vermont"],
    ["VA", "Virginia"],
    ["WA", "Washington"],
    ["WV", "West Virginia"],
    ["WI", "Wisconsin"],
    ["WY", "Wyoming"],
]


def bisection_approx(a, b, tol, maxIteration, f):
    # use bisection method to find the closest approximation for the reprdouction rate of a region
    i = 1
    tol = 0.01
    f_a = f(a)
    p = b
    # print(
    #     "%-5s %-10s %-10s %-10s %-10s %-10s" % ("i", "a", "b", "p", "f_p", "rel_error")
    # )

    while i < maxIteration:
        p_temp = p
        p = a + (b - a) / 2
        f_p = f(p)
        # print(str(p) + " " + str(p_temp))

        if f_p == 0 or (b - a) / 2 < tol:
            print("solution:" + str(p))
            r0 = p
            return r0
        # if p != 0:
        #     rel_error = abs(p - p_temp) / p
        #     print(a, b)
        #     print(
        #         "%-5.0f %-5.8f %-5.8f %-5.8f %-5.8f %5.8f"
        #         % (i, a, b, p, f_p, rel_error)
        #     )
        # else:
        #     print(a, b)
        #     print("%-5.0f %-5.8f %-5.8f %-5.8f %-5.8f %5.8f" % (i, a, b, p, f_p, 0))

        i += 1

        if (f_a - f_p) > 0:
            a = p
            f_a = f_p
        else:
            b = p


r0_set = []
for i in range(0, len(state_map)):
    state_abb = state_map[i][0]
    state_name = state_map[i][1]
    # state_abb = "MT"
    # state_name = "Montana"
    print(state_abb, state_name)
    state_data = filterDataForState(state_name, state_abb, covid_data)

    # getting the total population for the state
    total_pop = getPopulationForState(state_name)
    # stay_at_home_date = getDateOfStartOfOrder(state_name)
    # if stay_at_home_date == None:
    stay_at_home_date = "1/22/2020"
    stay_at_home_date_obj = datetime.strptime(
        stay_at_home_date, "%m/%d/%Y"
    ).date() + timedelta(days=14)
    df = filterDataByDate(state_data, stay_at_home_date_obj)

    actual_data = []
    for i in df.index:
        actual_data.append(df["Confirmed"][i])

    # calculating the SIR values given the parameters
    initial_cases = df["Confirmed"][0]
    inital_recovered = df["Recovered"][0]
    recovery_days = 14
    days = len(df.index)

    # function is defined as finding the SIR approximation and then finding the square diff from the actual vs the approximated
    def f(r0):
        S, I, R = SIR(total_pop, initial_cases, inital_recovered, 14, r0, days)
        SIR_data = []
        for y in I:
            SIR_data.append(y)
        return square_difference(actual_data, SIR_data)
    # r0 = bisection_approx(0, 6, 0.01, 50, f)
    r0 = 0
    for i in range(0, 1200):
        if f(i * 0.005) < f(r0):
            r0 = i * 0.005

    S, I, R = SIR(total_pop, initial_cases, inital_recovered, 14, r0, days)
    r0_set.append([state_name, r0])
print(r0_set)

# plotCases(I, actual_data, days, state_name)
