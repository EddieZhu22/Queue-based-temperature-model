import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from time import perf_counter
import timehorizonestimator

# convert to dataframe
df = pd.read_csv("datasets\data3.csv")

# input variables


g_cuttoff = 17

# statistics visualization
g_ps = []
g_slopes = []
tempdiff_arr = []
g_mtrs = []
avg_mu = []
avg_lambda = []
mu_diff = []
lambda_diff = []
day_arr = list(range(0, 365))
# end


def first_order_model(timehorizon):
    day = 0
    temperatureDayArr = []
    GHIDayArr = []
    for i in np.arange(int(len(df['Minute']))):
        if (df['Minute'][i] % 1440 == 0):
            if (day > 0):
                t0, t3 = timehorizonestimator.findt0t2t3(
                    temperatureDayArr, g_cuttoff)
                t2 = int(1/3*t0 + 2/3 * t3)
                g_ps.append((t3-t0)/10)

                sensitivity_analysis(max(temperatureDayArr),
                                     g_cuttoff, g_ps[len(g_ps)-1])

                mut0t2 = 0
                sum_lambda = 0
                netflow = 0
                netflowt2t3 = 0
                sum_netflow = 0
                sum_mu = 0
                sum_lambda = 0
                slope = 1  # guessed
                eqn_queue = []
                mu_arr = []

                # t0 t2
                for k in np.arange(int(t0/timehorizon), int(t2/timehorizon)+1):
                    mut0t2 = ((GHIDayArr[int(t2/timehorizon)]-GHIDayArr[int(t0/timehorizon)])/(
                        (t2-t0)/timehorizon))*(k-t0/timehorizon)+GHIDayArr[int(t0/timehorizon)]
                    mu_arr.append(mut0t2)
                    sum_mu += mut0t2
                    netflow = GHIDayArr[int(k)] - mut0t2
                    sum_netflow += netflow

                queue = sum_netflow

                # total lambda for t2 t3
                for k in np.arange(int(t2/timehorizon), int(t3/timehorizon)+1):
                    sum_lambda += GHIDayArr[int(k)]

                # approximate slope
                func_approx(slope, sum_netflow, GHIDayArr[int(
                    int(t2/timehorizon))], GHIDayArr, sum_lambda, t2, t3, timehorizon, .2)

                # total lambda for t2 t3
                for k in np.arange(int(t0/timehorizon), int(t2/timehorizon)+1):
                    sum_lambda += GHIDayArr[int(k)]

                slope = g_slopes[len(g_slopes) - 1]

                # t2 - t3
                for k in np.arange(0, int(t3/timehorizon)-int(t2/timehorizon)):
                    y = slope*k + GHIDayArr[int(int(t2/timehorizon))]
                    sum_mu += y
                    netflowt2t3 = GHIDayArr[int(k) + int(t2/timehorizon)] - y
                    queue += netflowt2t3

                avg_mu.append((1 / (t3-t0)) * sum_mu)
                avg_lambda.append((1 / (t3-t0)) * sum_lambda)
                # eqn 1.1 (given)
                for k in np.arange(int(t0/timehorizon), int(t3/timehorizon)+1):
                    y = 1/3*((k - int(t0/timehorizon))**2) * \
                        (int(t3/timehorizon) - k)
                    eqn_queue.append(y)
                    mu_arr.append(y)
                mu_diff.append(
                    mu_arr[int(t2/timehorizon)-int(t0/timehorizon)] - mu_arr[0])
                lambda_diff.append(
                    GHIDayArr[int(t2/timehorizon)] - GHIDayArr[int(t0/timehorizon)])

                # print(eqn_queue)
                #print("queue t2 t3: " + str(queue))
                #print("queue t0 t2: " + str(sum_netflow))

            temperatureDayArr.clear()
            GHIDayArr.clear()
            day += 1
        temperatureDayArr.append(df['Average of Temperature'][i])
        GHIDayArr.append(df['Average of GHI'][i])


def sensitivity_analysis(maxtemp, cuttoff, p):
    # mtr = magnitude of temperature reduction
    tempdiff = maxtemp - cuttoff
    mtr = tempdiff/cuttoff
    tempdiff_arr.append(tempdiff)
    g_mtrs.append(mtr)


def plot_p():
    # Plot inflow rate
    fig = plt.figure()
    plt.plot(g_ps, 'r-', linewidth=3, label='Inflow rate')
    plt.ylabel('Hot Period (p)', fontsize=12)
    plt.xlabel('Day', fontsize=12)
    fig.savefig('Figures/p_plot.png', dpi=300, bbox_inches='tight')
    plt.show()

# inputs: x and input_val
# input value


def kdaysmoothing(x, input_val):
    agg_x = []
    y = []
    for i in np.arange(len(x)):

        total = 0
        average = 0
        count = 0

        for k in np.arange(len(x)):
            if (x[i] == x[k]):
                total += input_val[k]
                count += 1
        # since count is greater than 0, p value must exist
        if (count > 0):
            average = total / count
            dupe = False
            for j in range(len(y)):
                if (average == y[j]):
                    dupe = True
            if (dupe == False):
                y.append(average)
                agg_x.append(x[i])
    return agg_x, y


def plot_mtr():
    # Plot inflow rate
    ps, agg_mtr_vals = kdaysmoothing(g_ps, g_mtrs)

    cubic_fit = np.polyfit(ps, agg_mtr_vals, 2)
    p = np.poly1d(cubic_fit)
    xp = np.linspace(0, 144, 100)

    fig = plt.figure()

    plt.plot(g_ps, g_mtrs, '.', color='black', markersize=3)
    plt.scatter(ps, agg_mtr_vals, s=30, facecolors='none', edgecolors='r')

    plt.plot(xp, p(xp), '-', label='lienar')
    plt.legend(['Data', 'Mean Value Of Same P',
               'Estimated Curve'], loc='upper left')

    plt.xlabel('Hot Period (p)', fontsize=12)
    plt.ylabel('Magnitude Of Temperature Reduction', fontsize=12)
    plt.grid()

    plt.show()
    fig.savefig('Figures/mtr_vs_p.svg')


def plot_mu(x, x_var_name, bounds):

    agg_x, agg_mu = kdaysmoothing(x, mu_diff)

    cubic_fit = np.polyfit(agg_x, agg_mu, 2)
    p = np.poly1d(cubic_fit)
    xp = np.linspace(0, bounds, 500)

    fig = plt.figure()

    plt.plot(x, mu_diff, '.', color='black', markersize=3)

    plt.scatter(agg_x, agg_mu, s=30, facecolors='none', edgecolors='r')

    plt.plot(xp, p(xp), '-', label='lienar')
    plt.legend(['Data', 'Mean Value Of Same ' + x_var_name,
               'Estimated Curve'], loc='upper left')

    plt.title('Difference Mu ' + 'vs ' + x_var_name)
    plt.xlabel(x_var_name, fontsize=12)
    plt.ylabel('Difference Mu', fontsize=12)
    plt.grid()

    plt.show()
    #fig.savefig('Figures/avg_mu' + str(id(x)) + '.png')
    # approximates function from area bound and lambda(t)


def func_approx(slope, netflow, lambdat2, lambda_arr, total_lambda, t2, t3, timehorizon, step):
    total_mu = 0
    curr_netflow = 0
    queue = 0
    #y = mx+b
    # loops through a guessed slope and finds final queue
    for k in np.arange(0, int(t3/timehorizon)-int(t2/timehorizon)):
        y = slope*k + lambdat2
        # print(y)
        total_mu += y
        curr_netflow = y - lambda_arr[k + int(t2/timehorizon)]
        queue += curr_netflow

    # if the queue - netflow is within reasonable error return the correct linear slope

    if (abs(queue - netflow) < 1):
        #print("final slope: " + str(slope))
        #print("final netflow: " + str(netflow))
        print("error: " + str(queue - netflow))
        #print("final queue: " + str(queue))
        g_slopes.append(slope)
    else:
        try:
            #print("slope: " + str(slope))
            #print("queue: " + str(queue))
            #print("netflow: " + str(queue - netflow))
            if (queue < netflow):
                slope += step
            if (queue > netflow):
                slope -= step

            # occassionaly breaks. There is probably a better method of attaining the correct answer
            if (abs(queue - netflow) < 500):
                step /= 1.005
            if (queue == 0.0):
                g_slopes.append(0)
            else:
                func_approx(slope, netflow, lambdat2, lambda_arr,
                        total_lambda, t2, t3, timehorizon, step)
        except:
            #print("netflow: " + str(queue - netflow))
            g_slopes.append(0)
if __name__ == "__main__":
    t1_start = perf_counter()
    first_order_model(10)
    t1_stop = perf_counter()
    # plot_p()
    # plot_mtr()
    plot_mu(day_arr, "Day", 365)
    print("Elapsed time:", t1_stop - t1_start)
