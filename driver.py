from getdata import *
from sir import *
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from plot import *

# this the driver class where all the code will be run from
# getting the inital data from the github repo
covid_data = getDataFromUS()
state_data = filterDataForState("Nebraska", "NE", covid_data)

# getting the total population for the state
total_pop = getPopulationForState("Nebraska")
stay_at_home_date = getDateOfStartOfOrder("Nebraska")
if stay_at_home_date == None:
    stay_at_home_date = "1/22/2020"
    print("no stay ath ome order")
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


r0 = 0
# use bisection method to find the closest approximation for the reprdouction rate of a region
a = 0
b = 6
i = 1  # iteration counter
tol = 0.01
maxIteration = 50
f_a = f(a)
p = b
print("%-5s %-10s %-10s %-10s %-10s %-10s" % ("i", "a", "b", "p", "f_p", "rel_error"))

while i < maxIteration:
    p_temp = p
    p = a + (b - a) / 2
    f_p = f(p)
    # print(str(p) + " " + str(p_temp))

    if f_p == 0 or (b - a) / 2 < tol:
        print("solution:" + str(p))
        r0 = p
        break
    # if p != 0:
    #     rel_error = abs(p - p_temp) / p
    #     # print(a, b)
    #     # print("%-5.0f %-5.8f %-5.8f %-5.8f %-5.8f %5.8f" % (i, a, b, p, f_p, rel_error))
    # else:
    #     # print(a, b)
    #     # print("%-5.0f %-5.8f %-5.8f %-5.8f %-5.8f %5.8f" % (i, a, b, p, f_p, 0))

    i += 1

    if (f_a - f_p) > 0:
        a = p
        f_a = f_p
    else:
        b = p

S, I, R = SIR(total_pop, initial_cases, inital_recovered, 14, r0, days)
plotCases(I, actual_data, days)
