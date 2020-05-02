import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.dates import YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange
import math

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
def plotCases(
    SIR_pre, SIR_post, actual_pre, actual_post, state_name, days_pre, days_post
):
    t = list(range(days_post + days_pre))
    for i in range(days_post):
        SIR_pre.append(np.NaN)
        actual_pre.append(np.NaN)
    for i in range(days_pre):
        SIR_post.insert(0, np.NaN)
        actual_post.insert(0, np.NaN)

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, SIR_pre, "r", alpha=0.5, lw=2, label="SIR Predicted Before Order")
    ax.plot(t, actual_pre, alpha=0.5, lw=2, label="Actual Data Before Order")

    ax.plot(t, SIR_post, "g", alpha=0.5, lw=2, label="SIR Predicted After")
    ax.plot(t, actual_post, alpha=0.5, lw=2, label="Actual Data After")
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


def plotBefore(SIR_pre, actual_pre, state_name):
    t = list(range(len(SIR_pre)))
    # print(len(t), len(SIR_pre), len(actual_pre))
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, SIR_pre, "r", lw=2, label="SIR Predicted Before Order")
    ax.plot(t, actual_pre, lw=2, label="Actual Data Before Order")
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

    plt.savefig("graphs\\" + str(state_name) + str("_pre.png"))


def plotAfter(SIR_post, SIR_if, actual_post, state_name):
    t = list(range(len(SIR_post)))
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, SIR_post, "g", lw=2, label="SIR Predicted After")
    ax.plot(t, actual_post, lw=2, label="Actual Data After")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number of Cases")
    ax.set_ylim()
    ax.plot(t, SIR_if, "r", alpha=0.5, lw=2, label="SIR Continued")

    ax.set_title(state_name)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    plt.savefig("graphs\\" + str(state_name) + str("_post.png"))


def plotPoly(cases, coefficients, state_name, exp):
    t = list(range(len(cases)))
    y = []

    if exp:
        for x in t:
            approx = coefficients[1] * math.e ** (coefficients[0] * x)
            y.append(approx)
    else:
        for x in t:
            approx = 0
            for i in range(0, len(coefficients)):
                approx = approx + coefficients[i] * x ** i
            y.append(approx)

    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, y)
    ax.plot(t, cases, lw=2, label="Actual Data")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number of Cases")
    ax.set_ylim()
    ax.set_title(state_name)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    plt.show()
    # plt.savefig("graphs\\" + str(state_name) + str("_polyfit.png"))
