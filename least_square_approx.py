import math
import sys
import numpy
from scipy.integrate import quad
from tabulate import tabulate

data = [
    [0.1, 0.53758],
    [0.2, 0.66472],
    [0.3, 1.17337],
    [0.4, 1.50877],
    [0.5, 1.62040],
    [0.6, 1.72621],
    [0.7, 1.87799],
    [0.8, 1.99043],
    [0.9, 2.17628],
    [1, 1.91595],
]

data1 = [[1, 1.36], [1.25, 1.91], [1.5, 2.19], [2, 3.74], [2.5, 4.63]]

test_data = [[0, 1], [0.25, 1.2840], [0.5, 1.6487], [0.75, 2.1170], [1, 2.7183]]

exp_data = [[1, 5.1], [1.25, 5.79], [1.5, 6.53], [1.75, 7.45], [2, 8.46]]

# given data points, this will return what the point should be at with the calcualted linear approximation with the data
def lin_approx(data, table):
    x_i_sum, y_i_sum, x_i_squared_sum, x_i_y_i_sum, m = 0, 0, 0, 0, 0

    # finding the summmations needed to solve for the coefficients
    for point in data:
        m = m + 1
        x = point[0]
        y = point[1]

        x_i_sum = x + x_i_sum
        y_i_sum = y + y_i_sum
        x_i_squared_sum = x_i_squared_sum + x ** 2
        x_i_y_i_sum = x_i_y_i_sum + (x * y)

    # solving for the coefficients
    a_0 = (x_i_squared_sum * y_i_sum - x_i_y_i_sum * x_i_sum) / (
        m * x_i_squared_sum - x_i_sum ** 2
    )
    a_1 = (m * x_i_y_i_sum - x_i_sum * y_i_sum) / (m * x_i_squared_sum - x_i_sum ** 2)

    if table:
        print(
            "Table for Linear Approximation: \n"
            + tabulate(
                [
                    [
                        round(x_i_sum, 4),
                        round(y_i_sum, 4),
                        round(x_i_squared_sum, 4),
                        round(x_i_y_i_sum, 4),
                        round(a_1, 4),
                        round(a_0, 4),
                    ]
                ],
                floatfmt=".4f",
                headers=[
                    "Sum of x",
                    "Sum of y",
                    "Sum of x^2",
                    "Sum of xy",
                    "a1",
                    "a0",
                ],
                tablefmt="pretty",
            )
        )

    # finding the approximation given the points
    return a_1, a_0


def exp_approx(data):
    x_i_sum, y_i_sum, x_i_squared_sum, x_i_y_i_sum, m = 0, 0, 0, 0, 0

    # finding the summmations needed to solve for the coefficients
    for point in data:
        m = m + 1
        x = point[0]
        y = point[1]

        x_i_sum = x + x_i_sum
        y_i_sum = y_i_sum + math.log(y, math.e)
        x_i_squared_sum = x_i_squared_sum + x ** 2
        x_i_y_i_sum = x_i_y_i_sum + (x * math.log(y, math.e))

    # solving for the coefficients
    a_0 = (x_i_squared_sum * y_i_sum - x_i_y_i_sum * x_i_sum) / (
        m * x_i_squared_sum - x_i_sum ** 2
    )
    a_1 = (m * x_i_y_i_sum - x_i_sum * y_i_sum) / (m * x_i_squared_sum - x_i_sum ** 2)

    # b = e^a_0
    b = math.e ** a_0

    # finding the approximation given the points
    return a_1, b


def poly_approx(data, power):
    # depending on the power, find the appropriate number of summations
    x_sum = []  # table for holding all the x-summations
    xy_sum = []  # table for holding all the xy-summation

    # calculating all the coefficients for solving the system
    # need to calculate sums from x^0 to x^2n
    for i in range(0, power * 2 + 1):
        pow = i
        x_total = 0
        xy_total = 0

        # going through each point to get a running total
        for point in data:
            x = point[0]
            y = point[1]
            x_total = x_total + x ** pow
            if i <= power:  # only need coefficients for a0 .. an
                xy_total = xy_total + (x ** pow * y)
        x_sum.append(x_total)
        if i <= power:
            xy_sum.append(xy_total)

    # building the system of equations
    # building the coefficient matrix
    A = []
    for j in range(0, power + 1):
        A_row = []
        for k in range(0, power + 1):
            A_row.append(x_sum[j + k])
        A.append(A_row)

    # solving for the system of equations
    a = numpy.array(A)
    b = numpy.array(xy_sum)
    # print("A Coefficient Matrix\n" + str(a))
    # print("B Matrix\n " + str(b))
    x = numpy.linalg.solve(a, b)
    # print("Coefficients: " + str(x))

    return x
    # # finding the approximation at the point x_0
    # approx = 0
    # for i in range(0, power + 1):
    #     approx = approx + x[i] * x_0 ** i

    # return approx


def error(actual, approximation):
    return str(round(abs(actual - approximation) / actual * 100, 4)) + "%"

# lin_approx(data1, 2.25,True)
"""
approx = []
actual = 1.921875
linear = lin_approx(data, 0.75, False)
lin_info = ["Linear", linear, error(actual, linear)]
print("Quadratic")
quad = poly_approx(data, 2, 0.75)

print("\nCubic")
cube = poly_approx(data, 3, 0.75)
quad_info = ["Quadratic", quad, error(actual, quad)]
cube_info = ["Cubic", cube, error(actual, cube)]
approx = [lin_info, quad_info, cube_info]
print()
print(
    "Final Results for Least Squares Approximations:\n"
    + tabulate(
        approx,
        headers=["Least Squares Power", "Estimated Value", "Relative Error"],
        tablefmt="pretty",
    )
)"""
