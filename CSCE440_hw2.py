import csv
import math


def Legrange(points, x_0):

    estimation = 0
    # constructing the L_i(x) * f(x_i) then adding onto a running total
    for i in range(0, len(points)):
        # constructing L_i(x)
        numerator = 1
        denominator = 1
        for k in range(0, len(points)):
            if (k != i):
                numerator *= (x_0 - points[k][0])
                denominator *= (points[i][0] - points[k][0])
        # calculating L_i(x)
        L_i = numerator/denominator
        # print(str(i) + " " + str(L_i))

        # adding L_i(x) * f(x_i) to the running total
        estimation += L_i * points[i][1]
        # print(str(i) + " " + str(points[i][1]))

    print("Final estimation from Legrange: " + str(round(estimation, 5)))


def Nevilles(points, x_0):

    q = []
    for i in range(0, len(points)):
        qq = []
        for j in range(0, i+1):
            if (j == 0):
                qq.append(points[i][1])
            else:
                qq.append(0)
        q.append(qq)

    for i in range(1, len(points)):
        for j in range(0, i+1):
            if (j == 0):
                q[i][j] = points[i][1]
            else:

                q[i][j] = round((((x_0 - points[i-j][0])*q[i][j-1]
                                  - (x_0 - points[i][0])*q[i-1][j-1])
                                 / (points[i][0] - points[i-j][0])), 5)
    writeToCSV(q)
    print("Final estimation from Nevilles: " +
          str(q[len(points) - 1][len(points) - 1]))


def Newtons_Divided(points, x_0):
    f = []
    for i in range(0, len(points)):
        f_row = []
        for j in range(0, len(points)):
            if (j == 0):
                f_row.append(points[i][1])
            else:
                f_row.append(0)
        f.append(f_row)

    for i in range(0, len(points)):
        for j in range(0, len(points) - i):
            if (i > 0):
                f[j][i] = ((f[j+1][i-1] - f[j][i-1]) /
                           (points[j+i][0] - points[j][0]))

    writeToCSV(f)
    # building the polynomial with the coefficients in the table
    total = 0
    for i in range(0, len(points)):
        p = f[0][i]
        if (i > 0):
            for j in range(0, i):
                p *= (x_0 - points[j][0])
        total += p

    divided_out = str(f[0][0]) + " + "
    for i in range(1, len(points)):
        divided_out += str(round(f[0][i], 5))
        for j in range(0, i):
            divided_out += "(x-" + str(round(points[j][0], 5)) + ")"
        if i < len(points) - 1:
            divided_out += " + "
    print(divided_out)
    print("Final estimation from Newton's: " + str(round(total, 5)))


def Hermites(points, derivatives, x_0):
    n = len(points)
    Q = [[None for i in range(2*n)] for j in range(2*n)]
    z = [None for i in range(2*n)]

    for i in range(0, n):
        z[2 * i] = points[i][0]
        z[2 * i + 1] = points[i][0]

        Q[2 * i][0] = points[i][1]
        Q[2 * i + 1][0] = points[i][1]
        Q[2 * i + 1][1] = derivatives[i]

        if i != 0:
            Q[2 * i][1] = (Q[2 * i][0] - Q[2 * i - 1][0]) / \
                (z[2 * i] - z[2 * i - 1])

    for i in range(2, 2*n):
        for j in range(2, i+1):
            Q[i][j] = (Q[i][j-1] - Q[i-1][j-1])/(z[i] - z[i-j])

    estimation = Q[0][0]
    hermites = str(Q[0][0]) + "+"
    for i in range(1, 2*n):
        subtotal = Q[i][i]
        hermites += (str(round(Q[i][i], 5)))
        for j in range(0, i):
            subtotal *= (x_0 - z[j])
            hermites += "(x-" + str(z[j]) + ")"
        estimation += subtotal
        if (i < 2*n - 1):
            hermites += "+"

    for i in range(0, len(Q)):
        for j in range(0, len(Q[i])):
            if (Q[i][j] != None):
                Q[i][j] = round(Q[i][j], 5)
    writeToCSV(Q)

    print(hermites)
    print("Final estimation from Hermite's: " + str(round(estimation, 5)))


def Natural_Spline(points):

    n = len(points)
    h = [None] * (n-1)
    for i in range(0, n-1):
        h[i] = points[i+1][0] - points[i][0]

    alpha = [None] * (n-1)
    for i in range(1, n-1):
        alpha[i] = ((3/h[i] * (points[i+1][1] - points[i][1])) -
                    ((3/h[i-1]) * (points[i][1] - points[i-1][1])))
    l = [None] * (n)
    mew = [None] * (n-1)
    z = [None] * (n)

    l[0] = 1
    mew[0] = 0
    z[0] = 0

    for i in range(1, n-1):
        l[i] = ((2 * (points[i+1][0] - points[i-1][0]) - h[i-1] * mew[i-1]))
        mew[i] = (h[i]/l[i])
        z[i] = ((alpha[i] - h[i-1] * z[i-1])/(l[i]))
    l[n-1] = 1
    z[n-1] = 0
    c = [None] * n
    c[n-1] = 0
    b = [None] * (n-1)
    d = [None] * (n-1)
    for j in range(n-2, -1, -1):
        c[j] = z[j] - mew[j] * c[j+1]
        b[j] = (points[j+1][1] - points[j][1]) / \
            h[j] - h[j] * (c[j+1] + 2 * c[j])/3
        d[j] = (c[j+1] - c[j])/(3 * h[j])

    for i in range(0, n-1):
        x_0 = points[i][0]
        print(str(round(points[i][1], 5)) + "+" + str(round(b[i], 5)) + "(x-" + str(x_0) + ") + " + str(
            round(c[i], 5)) + "(x-" + str(x_0) + ")^2 + " + str(round(d[i], 5)) + "(x-" + str(x_0) + ")^3")


def Clamped_Spline(points, fpo, fpn):
    n = len(points)
    h = [None] * (n-1)
    for i in range(0, n-1):
        h[i] = points[i+1][0] - points[i][0]

    alpha = [None] * (n)
    alpha[0] = 3 * (points[1][1] - points[0][1])/h[0] - 3 * fpo
    alpha[n-1] = 3 * fpn - 3 * (points[n-1][1] - points[n-2][1])/h[n-2]

    for i in range(1, n-1):
        alpha[i] = ((3/h[i] * (points[i+1][1] - points[i][1])) -
                    ((3/h[i-1]) * (points[i][1] - points[i-1][1])))

    l = [None] * (n)
    mew = [None] * (n-1)
    z = [None] * (n)

    l[0] = 2 * h[0]
    mew[0] = 0.5
    z[0] = alpha[0]/l[0]

    for i in range(1, n-1):
        l[i] = ((2 * (points[i+1][0] - points[i-1][0]) - h[i-1] * mew[i-1]))
        mew[i] = (h[i]/l[i])
        z[i] = ((alpha[i] - h[i-1] * z[i-1])/(l[i]))

    l[n-1] = h[n-2] * (2 - mew[n-2])
    z[n-1] = (alpha[n-1]-h[n-2]*z[n-2])/l[n-1]
    c = [None] * n
    c[n-1] = z[n-1]
    b = [None] * (n-1)
    d = [None] * (n-1)

    for j in range(n-2, -1, -1):
        c[j] = z[j] - mew[j] * c[j+1]
        b[j] = (points[j+1][1] - points[j][1]) / \
            h[j] - h[j] * (c[j+1] + 2 * c[j])/3
        d[j] = (c[j+1] - c[j])/(3 * h[j])

    for i in range(0, n-1):
        x_0 = points[i][0]
        print(str(round(points[i][1], 5)) + "+" + str(round(b[i], 5)) + "(x-" + str(x_0) + ") + " + str(
            round(c[i], 5)) + "(x-" + str(x_0) + ")^2 + " + str(round(d[i], 5)) + "(x-" + str(x_0) + ")^3")


def writeToCSV(rows):
    # name of csv file
    filename = "hw2_out.csv"

    # writing to csv file
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the data rows
        csvwriter.writerows(rows)


def bezier(points, points_plus, points_minus):

    n = len(points)
    coefficients = []
    points_minus.insert(0, [None, None])

    for i in range(0, n - 1):
        a_0 = (points[i][0])
        b_0 = (points[i][1])
        a_1 = 3 * (points_plus[i][0] - points[i][0])
        b_1 = 3 * (points_plus[i][1] - points[i][1])
        a_2 = 3 * (points[i][0] + points_minus[i+1][0] - 2 * points_plus[i][0])
        b_2 = 3 * (points[i][1] + points_minus[i+1][1] - 2 * points_plus[i][1])
        a_3 = points[i+1][0] - points[i][0] + 3 * \
            points_plus[i][0] - 3 * points_minus[i+1][0]
        b_3 = points[i+1][1] - points[i][1] + 3 * \
            points_plus[i][1] - 3 * points_minus[i+1][1]
        coefficients_for_i = [a_0, b_0, a_1, b_1, a_2, b_2, a_3, b_3]
        coefficients.append(coefficients_for_i)

    print(coefficients)


test = [[0, 1], [1, math.e], [2, math.e ** 2], [3, math.e ** 3]]
sn1 = [[1, 30], [5, 33], [8, 35], [12, 27], [
    15, 29], [19, 32], [22, 35], [26, 37], [29, 39]]
sn2 = [[2, 36], [4, 35], [9, 30], [11, 28], [
    16, 34], [18, 32], [23, 36], [25, 37], [30, 40]]
sn3 = [[6, 42], [13, 36], [20, 38], [27, 40]]
sn4 = [[7, 32], [14, 34], [21, 36], [28, 35]]
sn5 = [[5, 28], [10, 30], [15, 33], [20, 31]]
sn6 = [[8, 30], [15, 37], [22, 42], [29, 44]]
sns = [sn1, sn2, sn3, sn4, sn5, sn6]
table2 = [[-2, 3.230639], [-1, -0.730600],
          [0, -0.633970], [1, 0.586080], [2, 12.03208]]
table3 = [[-0.2, -0.1697], [0, 1], [0.2, 2.2518]]
test_hermites = [[1.3, 0.6200860], [1.6, 0.4554022], [1.9, 0.2818186]]
derivatives_for_test_hermites = [-0.5220232, -0.5698959, -0.5811571]
derivatives_for_table_3 = [5.7406, 6, 6.5836]
bezier_points = [[3, 5], [6, 3], [8, 5]]
bezier_points_plus = [[1, 3], [7, 2]]
bezier_points_minus = [[5, 4], [9, 6]]


for sn in sns:
    Legrange(sn, 17)  # problem 4
    Nevilles(sn, 11)  # problem 5
    Newtons_Divided(sn, 7)  # problem 6

Natural_Spline(table2)  # problem 7
Clamped_Spline(table2, -9.97685, 22.60286)  # problem 7

Newtons_Divided(table3, 0.1)  # problem 8
Hermites(table3, derivatives_for_table_3, .1)  # problem 8

bezier(bezier_points, bezier_points_plus, bezier_points_minus)  # problem 9
