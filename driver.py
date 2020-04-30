from getdata import *
from sir import SIR
from datetime import timedelta

# this the driver class where all the code will be run from
# getting the inital data from the github repo
covid_data = getDataFromUS()
state_data = filterDataForState("New York", "NY", covid_data)
# getting the total population for the state
total_pop = getPopulationForState("New York")
stay_at_home_date = getDateOfStartOfOrder("New York")
print(stay_at_home_date)
filterDataByDate(state_data, stay_at_home_date)


# calculating the SIR values given the parameters
initial_cases = 1
inital_recovered = 0
recovery_days = 14
reproduction_rate_wo_social_distancing = 5.7
reproduction_rate_w_social_distancing = 1.5
days = 500
# SIR data w/o social distancing
S1, I1, R1 = SIR(
    total_pop,
    initial_cases,
    inital_recovered,
    recovery_days,
    reproduction_rate_wo_social_distancing,
    days,
)
# SIR data w/ social distancing
S2, I2, R2 = SIR(
    total_pop,
    initial_cases,
    inital_recovered,
    recovery_days,
    reproduction_rate_w_social_distancing,
    days,
)
