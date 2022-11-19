import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from time import perf_counter
import timehorizonestimator

# convert to dataframe
df = pd.read_csv("datasets\data3.csv") 


#statistics visualization
g_ps = []
slopes = []

# end

def first_order_model(timehorizon):
    day = 0
    temperatureDayArr = []
    GHIDayArr = []
    for i in np.arange(int(len(df['Minute']))):
        if(df['Minute'][i] % 1440 == 0):
            if(day > 0):
                t0, t3 = timehorizonestimator.findt0t2t3(temperatureDayArr,16)
                t2 = int(1/3*t0 + 2/3 * t3)
                g_ps.append(t3-t0)
                mut0t2 = 0
                sum_mut0t2 = 0
                sum_lambdat2t3 = 0
                netflow = 0
                netflowt2t3 = 0
                sum_netflow = 0
                slope = 1 # guessed
                eqn_queue = []
                
                
                # t0 t2
                for k in np.arange(int(t0/timehorizon),int(t2/timehorizon)+1):
                    mut0t2 = ((GHIDayArr[int(t2/timehorizon)]-GHIDayArr[int(t0/timehorizon)])/((t2-t0)/timehorizon))*(k-t0/timehorizon)+GHIDayArr[int(t0/timehorizon)]
                    sum_mut0t2 += mut0t2
                    netflow = GHIDayArr[int(k)] - mut0t2
                    sum_netflow += netflow
                
                queue = sum_netflow
                
                # total lambda for t2 t3
                for k in np.arange(int(t2/timehorizon),int(t3/timehorizon)+1):
                    sum_lambdat2t3 += GHIDayArr[int(k)]
                
                # approximate slope
                func_approx(slope,sum_netflow,GHIDayArr[int(int(t2/timehorizon))], GHIDayArr,sum_lambdat2t3,t2,t3,timehorizon,.2)
                
                slope = slopes[len(slopes) - 1 ]

                # t2 - t3
                for k in np.arange(0,int(t3/timehorizon)-int(t2/timehorizon)):
                    y = slope*k + GHIDayArr[int(int(t2/timehorizon))]
                    netflowt2t3 = GHIDayArr[int(k) + int(t2/timehorizon)] - y
                    queue += netflowt2t3
                    
                    
                # eqn 1.1 (given)
                for k in np.arange(int(t0/timehorizon),int(t3/timehorizon)+1):
                    y = 1/3*((k - int(t0/timehorizon))**2)*(int(t3/timehorizon) - k)
                    eqn_queue.append(y)
                
                #print(eqn_queue)
                #print("queue t2 t3: " + str(queue))
                #print("queue t0 t2: " + str(sum_netflow))

            temperatureDayArr.clear()
            GHIDayArr.clear();        
            day += 1
        temperatureDayArr.append(df['Average of Temperature'][i])
        GHIDayArr.append(df['Average of GHI'][i])
        
def plot_p():
    # Plot inflow rate
    fig = plt.figure()
    plt.plot(g_ps, 'r-', linewidth=3, label = 'Inflow rate')
    plt.ylabel('Hot Period (p)', fontsize=12)
    plt.ylabel('Day', fontsize=12)
    fig.savefig('../Figures/Inflow rate.png', dpi=300, bbox_inches='tight')
    plt.show()
    # approximates function from area bound and lambda(t)
def func_approx(slope,netflow,lambdat2, lambda_arr, total_lambda,t2,t3,timehorizon,step):
    total_mu = 0
    curr_netflow = 0
    queue = 0
    #y = mx+b
    #loops through a guessed slope and finds final queue
    for k in np.arange(0,int(t3/timehorizon)-int(t2/timehorizon)):
        y = slope*k + lambdat2
        #print(y)
        total_mu += y
        curr_netflow = y- lambda_arr[k + int(t2/timehorizon)]
        queue += curr_netflow
        
        
    # if the queue - netflow is within reasonable error return the correct linear slope
    
    if(abs(queue - netflow) < 1):
        print("final slope: " + str(slope))
        #print("final netflow: " + str(netflow))
        #print("final queue: " + str(queue))
        slopes.append(slope)
    else:
        #print("slope: " + str(slope))
        #print("queue: " + str(queue))
        #print("netflow: " + str(queue - netflow))
        if(queue < netflow):
            slope += step
        if(queue > netflow):
            slope -= step

        if(abs(queue - netflow) < 100): # occassionaly breaks. There is probably a better method of attaining the correct answer
            step /= 1.005
        if(queue == 0.0):
            slopes.append(0)
        else:
            func_approx(slope,netflow,lambdat2, lambda_arr,total_lambda,t2,t3,timehorizon,step)



if __name__=="__main__":
    t1_start = perf_counter()
    first_order_model(10)
    t1_stop = perf_counter()
    plot_p()
    print("Elapsed time:", t1_stop - t1_start)