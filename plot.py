import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# plots the two estimated curves
def plotAndCompare(t, S1, I1, R1, S2, I2, R2):
    # A grid of time points (in days)
    t = np.linspace(0, t, t)
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    # ax.plot(t, S1, "b", alpha=0.5, lw=2, label="Susceptible")
    ax.plot(t, I1, "r", alpha=0.5, lw=2, label="Infected")
    # ax.plot(t, R1, "g", alpha=0.5, lw=2, label="Recovered with immunity")
    # ax.plot(t, S2, "y", alpha=0.5, lw=2, label="Susceptible")
    ax.plot(t, I2, "c", alpha=0.5, lw=2, label="Infected")
    # ax.plot(t, R2, "m", alpha=0.5, lw=2, label="Recovered with immunity")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number")
    # ax.set_ylim(0,1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    plt.show()


# plotting the SIR models, the polynomail approximation, and the actual data
# SIR = data from SIR method
# actual_data = actual data taken for region
# number of days you want to plot in the future
def plotCases(SIR, actual_data, days, state_name):
    t_a = np.linspace(0, len(actual_data), len(actual_data))
    t = np.linspace(0, days, days)
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, SIR, "r", alpha=0.5, lw=2, label="SIR Predicted")
    ax.plot(t_a, actual_data, alpha=0.5, lw=2, label="actual data")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number of Cases")
    ax.set_title(state_name)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    # plt.savefig(str(state_name) + str("1.png"))
    plt.show()
