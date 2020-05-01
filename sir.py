import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# This code was taken from: https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
# All credit should go to this website
def SIR(
    total_pop, inital_infected, initial_recovered, recovery_rate, reproduction_rate, t
):
    # Total population, N.
    N = total_pop
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, R0 = inital_infected, initial_recovered
    # Reproduction Rate (5.7 w/o social distancing, 1.5 w social distancing)
    r0 = reproduction_rate
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0
    # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
    gamma = 1.0 / recovery_rate
    beta = gamma * r0

    # The SIR model differential equations.
    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    # A grid of time points (in days)
    t = np.linspace(0, t, t)

    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    return S, I, R


# finding the average difference between the SIR data and the actual data to approximate the accuracy of the reproduction rate
def square_difference(actual, SIR_data):
    square_diff = 0

    for i in range(0, len(actual)):
        square_diff = square_diff + (actual[i] - SIR_data[i]) ** 2

    return square_diff / len(actual)


def relative_error(actual, SIR_data):
    rel_avg = 0

    for i in range(0, len(actual)):
        rel_avg = rel_avg + (abs(actual[i] - SIR_data[i]) / actual[i])

    return rel_avg / len(actual)
