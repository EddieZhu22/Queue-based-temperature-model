import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn
import pandas as pd
from scipy.stats import gaussian_kde
#https://novagateway.org/Dashboard/Overview
#https://www.sciencedirect.com/science/article/pii/S0924271618301217

df = pd.read_csv('ExportedData/P_Model_Validation.csv')
x,y = df['P'], df['Est P']
# Calculate the point density
xy = np.vstack([x,y])
n_samples = len(xy)
std_dev = np.std(xy)
bandwidth = 1.06 * std_dev * n_samples ** (-1/5)

print("Bandwidth:", bandwidth)
'''
# Calculate the point density

x,y = df['P'], df['Est P']
# Calculate the point density
xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = x[idx], y[idx], z[idx]

fig, ax = plt.subplots()
sc = ax.scatter(x, y, c=z, s=20,alpha = 0.7,cmap="jet")

b, m = 0.0449,0.9967
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
plt.title("Estimated Congestion Duration 'P' vs Observed 'P'")
plt.xlabel('Observed P (Hours)')
plt.ylabel('Estimated P (hours)')

ax.annotate("R-Squared = {:.3f}".format(0.9043), (1, 12))
ax.annotate("MAPE = {:.3f}%".format(11.29), (1, 11.5))
plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', linestyle='dotted', c = 'red', alpha = 0.7)
# norm = Normalize(vmin = np.min(z), vmax = np.max(z))
cbar = plt.colorbar(sc, alpha = 1)
cbar.set_label('Density')
plt.show()
fig.savefig('PvsEstP.png')'''


def density_scatter( x , y, ax = None, sort = True, bins = 20, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
    if ax is None :
        fig , ax = plt.subplots()
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True )
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)

    #To be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    sc = ax.scatter( x, y, c=z, **kwargs )
    b, m = 0.0449,0.9967
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.title("Estimated Congestion Duration 'P' vs Observed 'P'")
    plt.xlabel('Observed P (Hours)')
    plt.ylabel('Estimated P (hours)')

    ax.annotate("R-Squared = {:.3f}".format(0.9043), (1, 12))
    ax.annotate("MAPE = {:.3f}%".format(11.29), (1, 11.5))

    # plot y = m*x + b
    plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', linestyle='dotted', c = 'red', alpha = 0.7)
   # norm = Normalize(vmin = np.min(z), vmax = np.max(z))
    cbar = plt.colorbar(sc, alpha = 1)
    cbar.set_label('Density')

 
    fig.savefig('PvsEstP.png')
    return ax

'''
if "__main__" == __name__ :


    density_scatter( df['P'], df['Est P'], bins = [100,100], alpha = 0.5,s=10,cmap="jet")
    plt.show()
    
    '''

