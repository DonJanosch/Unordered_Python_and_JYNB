import numpy as np
import matplotlib.pyplot as plt

getClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))

x_range = np.logspace(-1,1,10,base=10)

y_assosiation = {0.1:1,0.99:1,0.25:1,0.5:0.5,0.75:0,200:0}

x_assosiation_sorted = sorted(list(y_assosiation.keys())) #This forces them to be in ascending order

if min(x_assosiation_sorted) < min(x_range) or max(x_assosiation_sorted) > max(x_range):
    print('The given Dictionary has elements which are out of the specified space-range, extrapolating linearly.')

y_assosiation_sorted = [y_assosiation[x] for x in x_assosiation_sorted]

y_result = [np.interp(x,x_assosiation_sorted,y_assosiation_sorted) for x in x_range]

plt.plot(y_result,'go-')
plt.show()

'''
for x in x_assosiation_sorted:
    y = y_assosiation[x]
    x_nearest = getClosest(x,x_range)
    y_nearest = np.where(x_range == x_nearest)
    if x > x_nearest:
        x_above = np.where(x_range > x_nearest)
        y_above = np.where(x_range == x_above)
        x2 = x_range[x_above[0][0]]
    elif x < x_nearest:
        x_below = np.where(x_range < x_nearest)
        y_below = np.where(x_range == x_below)
        x2 = x_range[x_below[0][-1]]
    else:
        x2 = x
        #we already found it, only must associate y with it
    print('x = {} / y = {} / x_nearest = {} / x_next = {}'.format(x,y,x_nearest,x2))

y_range = np.zeros_like(x_range)
'''
