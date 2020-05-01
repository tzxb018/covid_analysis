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

for i in range(0, len(state_map)):

    # getting the names of the state we are looking at
    state_abb = state_map[i][0]
    state_name = state_map[i][1]
    # state_abb = "WA"
    # state_name = "Washington"

    # obtaining the data specific for the state
    state_data = filterDataForState(state_name, state_abb, covid_data)

    # getting the start date and end date of the data set
    data_start_date = datetime.strptime(state_data.iloc[0]["Date"], "%m-%d-%Y").date()
    data_end_date = datetime.strptime(state_data.iloc[-1]["Date"], "%m-%d-%Y").date()

    # data sets to hold relevant data
    arr_pre = []
    arr_post = []
    arr_sir_pre = []
    arr_sir_post = []
    arr_r0 = []

    # getting the total population for the state
    total_pop = getPopulationForState(state_name)

    # determining if there has been a stay at home order issued
    stay_at_home_date = getDateOfStartOfOrder(state_name)
    if stay_at_home_date == None:

        # getting data for the range of time given
        df_pre_order = filterDataByDate(state_data, data_start_date, data_end_date)

        # filling in arrays with actual data
        for i in df_pre_order.index:
            arr_pre.append(df_pre_order["Confirmed"][i])

        # finding the reproductive rate before orders
        # setting the correct parameters
        initial_cases_pre = df_pre_order["Confirmed"][0]
        inital_recovered_pre = df_pre_order["Recovered"][0]
        recovery_days = 14
        days_pre = len(df_pre_order.index)

        # function is defined as finding the SIR approximation and then finding the square diff from the actual vs the approximated
        def f_pre(r0):
            S, I, R = SIR(
                total_pop, initial_cases_pre, inital_recovered_pre, 14, r0, days_pre
            )
            SIR_data = []
            for y in I:
                SIR_data.append(y)
            return square_difference(arr_pre, SIR_data)

        # determining the best fit r0 for pre-order
        pre_r0 = 0
        for i in range(0, 1200):
            if f_pre(i * 0.005) < f_pre(pre_r0):
                pre_r0 = i * 0.005

        # filling in the SIR data set with this r0
        S, I, R = SIR(
            total_pop, initial_cases_pre, inital_recovered_pre, 14, pre_r0, days_pre
        )
        for i in I:
            arr_sir_pre.append(i)

        arr_r0.append(round(pre_r0, 3))

    else:
        # since there is a stay at home order, we need to break the data in two sets
        # before the issued ordered, and 14 days after it was issued
        stay_at_home_date_obj = datetime.strptime(
            stay_at_home_date, "%m/%d/%Y"
        ).date() + timedelta(days=14)

        # getting data for pre/post order
        df_pre_order = filterDataByDate(
            state_data, data_start_date, stay_at_home_date_obj
        )
        df_post_order = filterDataByDate(
            state_data, stay_at_home_date_obj, data_end_date
        )

        # filling in arrays with actual data
        for i in df_pre_order.index:
            arr_pre.append(df_pre_order["Confirmed"][i])
        for i in df_post_order.index:
            arr_post.append(df_post_order["Confirmed"][i])

        # finding the reproductive rate before orders
        # setting the correct parameters
        initial_cases_pre = df_pre_order["Confirmed"][0]
        inital_recovered_pre = df_pre_order["Recovered"][0]
        recovery_days = 14
        days_pre = len(df_pre_order.index)

        # function is defined as finding the SIR approximation and then finding the square diff from the actual vs the approximated
        def f_pre(r0):
            S, I, R = SIR(
                total_pop, initial_cases_pre, inital_recovered_pre, 14, r0, days_pre
            )
            SIR_data = []
            for y in I:
                SIR_data.append(y)
            return square_difference(arr_pre, SIR_data)

        # determining the best fit r0 for pre-order
        pre_r0 = 0
        for i in range(0, 1200):
            if f_pre(i * 0.005) < f_pre(pre_r0):
                pre_r0 = i * 0.005

        # filling in the SIR data set with this r0
        S, I, R = SIR(
            total_pop, initial_cases_pre, inital_recovered_pre, 14, pre_r0, days_pre
        )
        for i in I:
            arr_sir_pre.append(i)

        arr_r0.append(round(pre_r0, 3))

        # finding the reporductive rate after orders
        # setting the correct parameters
        initial_cases_post = df_post_order["Confirmed"][0]
        inital_recovered_post = df_post_order["Recovered"][0]
        recovery_days = 14
        days_post = len(df_post_order.index)

        # function is defined as finding the SIR approximation and then finding the square diff from the actual vs the approximated
        def f_post(r0):
            S, I, R = SIR(
                total_pop, initial_cases_post, inital_recovered_post, 14, r0, days_post
            )
            SIR_data = []
            for y in I:
                SIR_data.append(y)
            return square_difference(arr_post, SIR_data)

        # determining the best fit r0 for pre-order
        post_r0 = 0
        for i in range(0, 1200):
            if f_post(i * 0.005) < f_post(post_r0):
                post_r0 = i * 0.005

        # filling in the SIR data set with this r0
        S, I, R = SIR(
            total_pop, initial_cases_post, inital_recovered_post, 14, post_r0, days_post
        )
        for i in I:
            arr_sir_post.append(i)

        arr_r0.append(round(post_r0, 3))

    print(state_name, arr_r0)
