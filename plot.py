import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.dates import YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange
import math
import csv

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

# function that plots the graphs of cubic polynomial
# returns the average derivative and second derivative of the polynomial
def plotPoly(cases, coefficients, state_name):
    t = list(range(len(cases)))
    y_change = []
    y = []
    sum_of_change2 = 0
    sum_of_change1 = 0
    for x in t:
        approx = 0

        # function for plotting the cubic fit
        for i in range(0, len(coefficients)):
            approx = approx + coefficients[i] * x ** i
        y.append(approx)

        approx_change = 0
        # function for plotting the derivative
        for i in range(1, len(coefficients)):
            approx_change = approx_change + i * coefficients[i] * x ** (i - 1)
        y_change.append(approx_change)
        sum_of_change1 = sum_of_change1 + approx_change

        approx2 = 0
        # function for finding the second derivative
        for i in range(2, len(coefficients)):
            approx2 = approx2 + i * (i - 1) * coefficients[i] * x ** (i - 2)

        sum_of_change2 = sum_of_change2 + approx2
    sum_of_change2 = sum_of_change2 / len(cases)
    sum_of_change1 = sum_of_change1 / len(cases)

    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ln1 = ax.plot(t, cases, "g", lw=2, label="Actual Data")
    ln2 = ax.plot(t, y, "b", lw=2, alpha=0.5, label="Least Square Cubic Fit")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number of Cases")
    ax.set_ylim()
    ax.set_title(state_name)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which="major", c="w", lw=2, ls="-")
    # plt.axvline(x=seperator)
    ax_derv = ax.twinx()

    ln3 = ax_derv.plot(t, y_change, ":", label="Change in Cases")
    ax_derv.set_ylabel("Change in Cases")
    ax_derv.set_ylim()

    lns = ln1 + ln2 + ln3
    labs = [l.get_label() for l in lns]
    legend = ax.legend(lns, labs, loc=0)
    legend.get_frame().set_alpha(0.5)
    for spine in ("top", "right", "bottom", "left"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    # plt.show()
    plt.savefig("graphs\\" + str(state_name) + str("_polyfit.png"))
    plt.close()

    return sum_of_change1, sum_of_change2


def plotExp(cases, coefficients_exp, coefficients_pow, state_name):
    t = list(range(len(cases)))
    y = []
    y_cub = []

    for x in t:
        approx = coefficients_exp[1] * math.e ** (coefficients_exp[0] * x)
        y.append(approx)

        approx = 0
        # function for plotting the cubic fit
        for i in range(0, len(coefficients_pow)):
            approx = approx + coefficients_pow[i] * x ** i
        y_cub.append(approx)

    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, y, "r:", lw=2, label="Exponential Fit")
    ax.plot(t, cases, "g", lw=2, label="Actual Data")
    ax.plot(t, y_cub, "b:", lw=2, label="Cubic Fit")
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
