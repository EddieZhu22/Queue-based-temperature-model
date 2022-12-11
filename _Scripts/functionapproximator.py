import numpy as np



def func_approx(slope, netflow, lambdat2, lambda_arr, total_lambda, t2, t3, timehorizon, step, g_slopes):
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
        #print("error: " + str(queue - netflow))
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