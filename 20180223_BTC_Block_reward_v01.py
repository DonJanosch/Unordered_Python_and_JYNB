import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Declare settings
headders = ['Halving Nr.','Starting year','Start-Block Nr.','End-Block Nr.','Current Blockreward','Total circulation at start of halving','Emission during halving','Percentage of total emission at end of halving']
btc_table = pd.DataFrame(columns = headders)

max_halvings = 33
initial_block_reward = 50 * 10**8
halving_interval = 210000
starting_year = 2009
circulation = 0
total_emission = 0

#Declare variables and placeholders
plt_year = []
plt_circulation = []

#Do calculate the mathematics
for halving in range(max_halvings):
    total_emission += 0.5**(halving+1)
    start_block = halving * halving_interval+1
    end_block = (halving+1) * halving_interval
    current_reward = int(int(10**8 * initial_block_reward * 0.5 ** halving)/10**8)
    emission = current_reward * halving_interval
    data_slice = pd.DataFrame([[halving,starting_year,start_block,end_block,current_reward/10**8,circulation/10**8,emission/10**8,total_emission*100]],columns = headders)
    btc_table= btc_table.append(data_slice)
    plt_year.append(starting_year)
    plt_circulation.append(circulation/10**8)
    starting_year +=4
    circulation += emission

max_circulation = circulation-emission
percentage_circulation = []
for e in plt_circulation:
    percentage_circulation.append(e/max_circulation*10**8*100)

#Update the results-table
btc_table = btc_table.set_index(headders[0])

#Print the results as text
linebreak = '\n#####\n'
print(linebreak,btc_table.head(),linebreak,btc_table.tail(),linebreak)

#Print the reults as graph
major_ticks = np.arange(2009,2141,8)
minor_ticks = np.arange(2009,2141,4)
y_major_ticks = np.arange(0,110,10)
y_minor_ticks = np.arange(0,100,5)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(plt_year,percentage_circulation, marker = 'x')
plt.title('BTC issuing over time, 100% = {} BTC'.format(max_circulation/10**8))
plt.xlabel('Year')
plt.ylabel('BTC in circulation in % of maximum')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor = True)
ax.set_yticks(y_major_ticks)
ax.set_yticks(y_minor_ticks, minor = True)
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
plt.grid(True)
plt.show()
