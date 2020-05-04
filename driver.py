from getdata import *
from sir import *
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from plot import *
import time
import csv
from least_square_approx import exp_approx, poly_approx

# this the driver class where all the code will be run from
# getting the inital data from the github repo
covid_data = getDataFromUS()

# state names and their abbriviations (for use as arguments)
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


def epidiomology(state_abb, state_name):
    # getting the names of the state we are looking at
    # state_name = state_map[i][1]
    # state_abb = state_map[i][0]
    state_abb = "CA"
    state_name = "California"

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
    arr_sir_if = []
    arr_r0 = []

    # getting the total population for the state
    total_pop = getPopulationForState(state_name)

    # determining if there has been a stay at home order issued
    stay_at_home_date = getDateOfStartOfOrder(state_name)
    if stay_at_home_date == None:

        return  # this can be commented out if want to find out info about states without saho

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
        days_post = 0

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
            state_data, stay_at_home_date_obj + timedelta(days=1), data_end_date
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

        # filling in the hypothetical data (r0 from before the order)
        Sif, Iif, Rif = SIR(
            total_pop, initial_cases_post, inital_recovered_post, 14, pre_r0, days_post
        )
        for i in Iif:
            arr_sir_if.append(i)

        arr_r0.append(round(post_r0, 3))

    print(state_name, arr_r0)
    with open("out.csv", "a") as out:
        writer = csv.writer(
            out, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        writer.writerow([state_abb, arr_r0[0], arr_r0[1]])

    # plotCases(
    #     arr_sir_pre, arr_sir_post, arr_pre, arr_post, state_name, days_pre, days_post
    # )
    plotBefore(arr_sir_pre, arr_pre, state_name)
    plotAfter(arr_sir_post, arr_sir_if, arr_post, state_name)


def least_square_approx(state_abb, state_name):
    # obtaining the data specific for the state
    state_data = filterDataForState(state_name, state_abb, covid_data)

    # getting the start date and end date of the data set
    data_start_date = datetime.strptime(state_data.iloc[0]["Date"], "%m-%d-%Y").date()
    data_end_date = datetime.strptime(state_data.iloc[-1]["Date"], "%m-%d-%Y").date()

    # data sets to hold relevant data
    arr_pre = []
    arr_post = []
    arr_cases = []

    # determining if there has been a stay at home order issued
    stay_at_home_date = getDateOfStartOfOrder(state_name)

    if stay_at_home_date != None:
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
            state_data, stay_at_home_date_obj + timedelta(days=1), data_end_date
        )

        # filling in arrays with actual data
        counter = 0
        c = 0
        for i in df_pre_order.index:
            arr_pre.append([counter, df_pre_order["Confirmed"][i]])
            arr_cases.append([c, df_pre_order["Confirmed"][i]])
            counter = counter + 1
            c = c + 1
        counter = 0
        for i in df_post_order.index:
            arr_post.append([counter, df_post_order["Confirmed"][i]])
            arr_cases.append([c, df_post_order["Confirmed"][i]])
            counter = counter + 1
            c = c + 1

        # getting the coefficients for the cubic function
        coeff_pre_exp = exp_approx(arr_pre)
        coeff_pre = poly_approx(arr_pre, 3)
        coeff_post = poly_approx(arr_post, 3)

        cases_pre = []
        cases_post = []
        for a in arr_pre:
            cases_pre.append(a[1])
        for b in arr_post:
            cases_post.append(b[1])

        pre1, pre2 = plotPoly(cases_pre, coeff_pre, str(state_name + " Before SAHO"))

        post1, post2 = plotPoly(cases_post, coeff_post, str(state_name + " After SAHO"))
        arr_change = [state_abb, pre1, pre2, post1, post2]

        # plotExp(cases_pre, coeff_pre_exp, coeff_pre, state_name)

        with open("results-from-cubic-fit.csv", "a", newline="") as out:
            writer = csv.writer(
                out, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            writer.writerow(arr_change)


# driver class
for state in state_map:
    epidiomology(state[0], state[1])
    least_square_approx(state[0], state[1])
