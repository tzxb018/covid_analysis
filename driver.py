from getdata import *
from sir import SIR
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt


# this the driver class where all the code will be run from
# getting the inital data from the github repo
covid_data = getDataFromUS()
state_data = filterDataForState("New York", "NY", covid_data)
# getting the total population for the state
total_pop = getPopulationForState("New York")
stay_at_home_date = getDateOfStartOfOrder("New York")
df = filterDataByDate(state_data, stay_at_home_date)

print(df["Confirmed"])
# calculating the SIR values given the parameters
initial_cases = df["Confirmed"][0]
inital_recovered = df["Recovered"][0]
recovery_days = 14
reproduction_rate_wo_social_distancing = 5.7
reproduction_rate_w_social_distancing = 1.5
days = 30
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


actual_data = []
for i in df.index:
    actual_data.append(df["Confirmed"][i])

t_a = np.linspace(0, len(df), len(df))
t = np.linspace(0, days, days)

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor="w")
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(t, I1, "r", alpha=0.5, lw=2, label="Infected")
ax.plot(t, I2, "g", alpha=0.5, lw=2, label="Infected")
ax.plot(t_a, actual_data )
ax.set_xlabel("Time /days")
ax.set_ylabel("Number of Cases")
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which="major", c="w", lw=2, ls="-")
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ("top", "right", "bottom", "left"):
    ax.spines[spine].set_visible(False)
plt.show()
